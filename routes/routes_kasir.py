from flask import Blueprint, render_template, request, redirect, session, jsonify
import mysql.connector
from functools import wraps
from datetime import datetime

kasir_bp = Blueprint('kasir', __name__, url_prefix='/kasir')

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="toko_cendrawasih"
    )

def kasir_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "kasir":
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@kasir_bp.route('/home')
@kasir_required
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stok_barang WHERE total_stok > 0 ORDER BY nama_barang")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('kasir.html', products=products)

@kasir_bp.route('/process_sale', methods=['POST'])
@kasir_required
def process_sale():
    cart_data = request.json
    
    if not cart_data or len(cart_data) == 0:
        return jsonify({"success": False, "message": "Keranjang kosong"}), 400
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        total_transaksi = 0
        
        for item in cart_data:
            cursor.execute("SELECT * FROM stok_barang WHERE kode_barang = %s", (item['kode_barang'],))
            product = cursor.fetchone()
            
            if not product or product['total_stok'] < item['qty']:
                db.rollback()
                cursor.close()
                db.close()
                return jsonify({"success": False, "message": f"Stok {item['nama_barang']} tidak cukup"}), 400
            
            harga_jual = float(item['harga_jual'])
            qty = int(item['qty'])
            subtotal = harga_jual * qty
            total_transaksi += subtotal
        
        cursor.execute(
            "INSERT INTO penjualan (tanggal_penjualan, kasir_id, total_transaksi) VALUES (%s, %s, %s)",
            (datetime.now().date(), session['user_id'], total_transaksi)
        )
        penjualan_id = cursor.lastrowid
        
        for item in cart_data:
            harga_jual = float(item['harga_jual'])
            qty = int(item['qty'])
            subtotal = harga_jual * qty
            
            cursor.execute(
                "INSERT INTO detail_penjualan (penjualan_id, kode_barang, nama_barang, qty, harga_jual, subtotal) VALUES (%s, %s, %s, %s, %s, %s)",
                (penjualan_id, item['kode_barang'], item['nama_barang'], qty, harga_jual, subtotal)
            )
            
            cursor.execute(
                "UPDATE stok_barang SET total_stok = total_stok - %s WHERE kode_barang = %s",
                (qty, item['kode_barang'])
            )
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({"success": True, "message": "Transaksi berhasil", "total": total_transaksi})
    
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()
        return jsonify({"success": False, "message": str(e)}), 500

@kasir_bp.route('/api/sales_history')
@kasir_required
def sales_history():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            p.id,
            p.tanggal_penjualan,
            p.total_transaksi,
            p.created_at,
            u.nama as kasir_nama
        FROM penjualan p
        JOIN users u ON p.kasir_id = u.id
        ORDER BY p.created_at DESC
        LIMIT 10
    """)
    
    sales = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(sales)

@kasir_bp.route('/api/sale_detail/<int:sale_id>')
@kasir_required
def sale_detail(sale_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM detail_penjualan WHERE penjualan_id = %s
    """, (sale_id,))
    
    details = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(details)
