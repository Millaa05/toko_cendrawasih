from flask import Blueprint, render_template, request, session, jsonify
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta

kepala_toko_bp = Blueprint('kepala_toko', __name__, url_prefix='/kepala_toko')

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="toko_cendrawasih"
    )

def kepala_toko_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "kepala_toko":
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@kepala_toko_bp.route('/home')
@kepala_toko_required
def home():
    return render_template('kepala_toko.html')

@kepala_toko_bp.route('/api/daily_report')
@kepala_toko_required
def daily_report():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    
    cursor.execute("""
        SELECT 
            DATE(tanggal_penjualan) as tanggal,
            SUM(total_transaksi) as total_penjualan,
            COUNT(*) as jumlah_transaksi
        FROM penjualan
        WHERE tanggal_penjualan >= %s
        GROUP BY DATE(tanggal_penjualan)
        ORDER BY tanggal DESC
    """, (start_date,))
    
    sales_data = cursor.fetchall()
    
    cursor.execute("""
        SELECT 
            DATE(tanggal_masuk) as tanggal,
            SUM(jumlah * harga_beli) as total_pembelian,
            COUNT(*) as jumlah_batch
        FROM barang_masuk
        WHERE tanggal_masuk >= %s
        GROUP BY DATE(tanggal_masuk)
        ORDER BY tanggal DESC
    """, (start_date,))
    
    purchase_data = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return jsonify({
        "sales": sales_data,
        "purchases": purchase_data
    })

@kepala_toko_bp.route('/api/stock_changes')
@kepala_toko_required
def stock_changes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            bm.kode_barang,
            bm.nama_barang,
            SUM(bm.jumlah) as stok_masuk,
            COALESCE(SUM(dp.qty), 0) as stok_keluar,
            (SUM(bm.jumlah) - COALESCE(SUM(dp.qty), 0)) as stok_akhir
        FROM barang_masuk bm
        LEFT JOIN detail_penjualan dp ON bm.kode_barang = dp.kode_barang
        GROUP BY bm.kode_barang, bm.nama_barang
        ORDER BY stok_akhir DESC
    """)
    
    changes = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(changes)
