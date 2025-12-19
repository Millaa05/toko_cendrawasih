from flask import Blueprint, render_template, request, redirect, session, jsonify
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta

gudang_bp = Blueprint('gudang', __name__, url_prefix='/gudang')

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="toko_cendrawasih"
    )

def gudang_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "gudang":
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@gudang_bp.route('/home')
@gudang_required
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM stok_barang")
    total_stock = cursor.fetchone()['total']
    
    cursor.close()
    db.close()
    
    return render_template('gudang.html', total_stock=total_stock)

@gudang_bp.route('/add_stock', methods=['POST'])
@gudang_required
def add_stock():
    data = request.json
    
    kode_barang = data.get('kode_barang')
    nama_barang = data.get('nama_barang')
    jumlah = int(data.get('jumlah'))
    harga_beli = float(data.get('harga_beli'))
    tanggal_kadaluarsa = data.get('tanggal_kadaluarsa')
    tanggal_masuk = data.get('tanggal_masuk', datetime.now().date())
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "INSERT INTO barang_masuk (kode_barang, nama_barang, jumlah, harga_beli, tanggal_kadaluarsa, tanggal_masuk) VALUES (%s, %s, %s, %s, %s, %s)",
            (kode_barang, nama_barang, jumlah, harga_beli, tanggal_kadaluarsa, tanggal_masuk)
        )
        
        cursor.execute("SELECT * FROM stok_barang WHERE kode_barang = %s", (kode_barang,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute(
                "UPDATE stok_barang SET total_stok = total_stok + %s, tanggal_kadaluarsa = %s, updated_at = NOW() WHERE kode_barang = %s",
                (jumlah, tanggal_kadaluarsa, kode_barang)
            )
        else:
            cursor.execute(
                "INSERT INTO stok_barang (kode_barang, nama_barang, total_stok, tanggal_kadaluarsa) VALUES (%s, %s, %s, %s)",
                (kode_barang, nama_barang, jumlah, tanggal_kadaluarsa)
            )
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({"success": True, "message": "Stok berhasil ditambahkan"})
    
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()
        return jsonify({"success": False, "message": str(e)}), 500

@gudang_bp.route('/api/stock_list')
@gudang_required
def stock_list():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            kode_barang,
            nama_barang,
            total_stok,
            tanggal_kadaluarsa,
            updated_at
        FROM stok_barang
        ORDER BY updated_at DESC
    """)
    
    stocks = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(stocks)

@gudang_bp.route('/api/alerts')
@gudang_required
def get_alerts():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    today = datetime.now().date()
    warning_date = today + timedelta(days=10)
    
    cursor.execute("""
        SELECT kode_barang, nama_barang, total_stok, tanggal_kadaluarsa,
               CASE 
                   WHEN tanggal_kadaluarsa < %s THEN 'expired'
                   WHEN tanggal_kadaluarsa <= %s THEN 'expiring'
               END as alert_type
        FROM stok_barang
        WHERE tanggal_kadaluarsa <= %s
        ORDER BY tanggal_kadaluarsa ASC
    """, (today, warning_date, warning_date))
    
    expiry_alerts = cursor.fetchall()
    
    cursor.execute("""
        SELECT s.kode_barang, s.nama_barang, s.total_stok, 
               COALESCE(f.reorder_point, 10) as rop
        FROM stok_barang s
        LEFT JOIN fsn_rop f ON s.kode_barang = f.kode_barang
        WHERE s.total_stok <= GREATEST(COALESCE(f.reorder_point, 10), 10)
    """)
    
    low_stock_alerts = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return jsonify({
        "expiry_alerts": expiry_alerts,
        "low_stock_alerts": low_stock_alerts
    })

@gudang_bp.route('/api/rop_analysis')
@gudang_required
def rop_analysis():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            s.kode_barang,
            s.nama_barang,
            s.total_stok,
            COALESCE(SUM(dp.qty), 0) as total_terjual,
            COALESCE(DATEDIFF(NOW(), MIN(p.tanggal_penjualan)), 1) as hari_jual,
            COALESCE(SUM(dp.qty) / NULLIF(DATEDIFF(NOW(), MIN(p.tanggal_penjualan)), 0), 0) as rata_harian
        FROM stok_barang s
        LEFT JOIN detail_penjualan dp ON s.kode_barang = dp.kode_barang
        LEFT JOIN penjualan p ON dp.penjualan_id = p.id
        GROUP BY s.kode_barang, s.nama_barang, s.total_stok
    """)
    
    products = cursor.fetchall()
    
    lead_time = 3
    safety_factor = 0.1
    min_rop = 10
    
    rop_data = []
    for p in products:
        rata_harian = float(p['rata_harian']) if p['rata_harian'] else 0
        safety_stock = rata_harian * safety_factor
        calculated_rop = (rata_harian * lead_time) + safety_stock
        
        rop = max(int(calculated_rop), min_rop)
        
        kategori_fsn = 'Non-moving'
        if rata_harian > 5:
            kategori_fsn = 'Fast'
        elif rata_harian > 1:
            kategori_fsn = 'Slow'
        
        cursor.execute("""
            INSERT INTO fsn_rop (kode_barang, nama_barang, kategori_fsn, rata_penjualan_harian, lead_time, reorder_point)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            kategori_fsn = %s,
            rata_penjualan_harian = %s,
            reorder_point = %s,
            updated_at = NOW()
        """, (p['kode_barang'], p['nama_barang'], kategori_fsn, rata_harian, lead_time, rop,
              kategori_fsn, rata_harian, rop))
        
        rop_data.append({
            'kode_barang': p['kode_barang'],
            'nama_barang': p['nama_barang'],
            'total_stok': p['total_stok'],
            'rata_penjualan_harian': round(rata_harian, 2),
            'kategori_fsn': kategori_fsn,
            'reorder_point': rop,
            'status': 'OK' if p['total_stok'] > rop else 'LOW'
        })
    
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify(rop_data)
