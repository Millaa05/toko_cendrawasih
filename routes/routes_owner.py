from flask import Blueprint, render_template, session, jsonify, redirect
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="toko_cendrawasih"
    )

def owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "owner":
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@owner_bp.route('/home')
@owner_required
def home():
    return render_template('owner.html')

@owner_bp.route('/api/summary')
@owner_required
def summary():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    today = datetime.now().date()
    
    cursor.execute("""
        SELECT 
            COALESCE(SUM(total_transaksi), 0) as total_penjualan_hari_ini
        FROM penjualan
        WHERE DATE(tanggal_penjualan) = %s
    """, (today,))
    
    today_sales = cursor.fetchone()
    
    cursor.execute("""
        SELECT 
            COALESCE(SUM(jumlah * harga_beli), 0) as total_pembelian_hari_ini
        FROM barang_masuk
        WHERE DATE(tanggal_masuk) = %s
    """, (today,))
    
    today_purchases = cursor.fetchone()
    
    cursor.execute("""
        SELECT 
            DATE(tanggal_penjualan) as tanggal,
            SUM(total_transaksi) as penjualan
        FROM penjualan
        WHERE tanggal_penjualan >= %s
        GROUP BY DATE(tanggal_penjualan)
        ORDER BY tanggal DESC
        LIMIT 7
    """, (today - timedelta(days=7),))
    
    weekly_sales = cursor.fetchall()
    
    cursor.execute("""
        SELECT 
            DATE(tanggal_masuk) as tanggal,
            SUM(jumlah * harga_beli) as pembelian
        FROM barang_masuk
        WHERE tanggal_masuk >= %s
        GROUP BY DATE(tanggal_masuk)
        ORDER BY tanggal DESC
        LIMIT 7
    """, (today - timedelta(days=7),))
    
    weekly_purchases = cursor.fetchall()
    
    profit = float(today_sales['total_penjualan_hari_ini']) - float(today_purchases['total_pembelian_hari_ini'])
    
    cursor.close()
    db.close()
    
    return jsonify({
        "today_sales": today_sales['total_penjualan_hari_ini'],
        "today_purchases": today_purchases['total_pembelian_hari_ini'],
        "today_profit": profit,
        "weekly_sales": weekly_sales,
        "weekly_purchases": weekly_purchases
    })
