from flask import Flask, render_template, request, redirect, url_for, session 
import mysql.connector
from functools import wraps
from routes.routes_kasir import kasir_bp
from routes.routes_gudang import gudang_bp
from routes.routes_kepala_toko import kepala_toko_bp
from routes.routes_owner import owner_bp

app = Flask(__name__)
app.secret_key = " "

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="toko_cendrawasih"
)
cursor = db.cursor(dictionary=True)

app.register_blueprint(kasir_bp)
app.register_blueprint(gudang_bp)
app.register_blueprint(kepala_toko_bp)
app.register_blueprint(owner_bp)

# ========== PROTECT ROUTE ==========
def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")
            if role and session.get("role") != role:
                return "Unauthorized Access"
            return f(*args, **kwargs)
        return decorated
    return wrapper


@app.route("/")
def index():
    return redirect("/login")


# ========== LOGIN ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            # Redirect sesuai role
            if user["role"] == "owner":
                return redirect("/owner/home")
            elif user["role"] == "kasir":
                return redirect("/kasir/home")
            elif user["role"] == "gudang":
                return redirect("/gudang/home")
            elif user["role"] == "kepala_toko":
                return redirect("/kepala_toko/home")

        else:
            msg = "Username atau Password Salah!"

    return render_template("login.html", msg=msg)

def ambil_kursor(dictionary=True):
    return db.cursor(dictionary=dictionary)

@app.route("/register", methods=["GET", "POST"])
def register():
    pesan = ""

    if request.method == "POST":
        nama = request.form.get("nama")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        # Validasi input kosong
        if not (nama and username and password and role):
            pesan = "Semua data harus lengkap!"
            return render_template("register.html", msg=pesan)

        k = ambil_kursor()

        # Cek username sudah ada atau belum
        k.execute("SELECT * FROM users WHERE username = %s", (username,))
        cek = k.fetchone()

        if cek:
            k.close()
            pesan = "Username sudah terdaftar!"
            return render_template("register.html", msg=pesan)

        try:
            k.execute(
                "INSERT INTO users (nama, username, password, role) VALUES (%s, %s, %s, %s)",
                (nama, username, password, role)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            k.close()
            pesan = f"Error database: {str(e)}"
            return render_template("register.html", msg=pesan)

        k.close()
        return redirect(url_for("login")) 

    return render_template("register.html", msg=pesan)


# ========== ADMIN HOME ==========
# Kepala Toko and Owner routes now handled by blueprints


# ========== LOGOUT ==========
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
