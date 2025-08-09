from sqlalchemy import create_engine, text, inspect

# kalau DB ada di folder lain, ganti ke path absolut, mis. sqlite:////full/path/spotify.db
engine = create_engine("sqlite:///spotify.db", echo=True, future=True)

try:
    with engine.connect() as conn:
        # 1) ping
        print("Ping:", conn.scalar(text("SELECT 1")))

        # 2) versi SQLite
        print("SQLite version:", conn.exec_driver_sql("SELECT sqlite_version()").scalar_one())

        # 3) daftar tabel
        insp = inspect(conn)
        print("Tables:", insp.get_table_names())
    print("✅ Koneksi OK")
except Exception as e:
    print("❌ Gagal konek:", e)