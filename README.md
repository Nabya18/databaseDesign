# Database Design for Spotify
- User accounts and subscriptions
- Artist, albums, songs
- track listens to a song
- Songs with multiple artists and genres
- follow artists and like songs

# Make relationship
- mapped_column(ForeignKey)
- relationship()
- Using back_populates is nice if you want to define the relationships on every class, so it's easy to see all the fields just be glancing at the model class.
- Define the many-to-many relationship using 'secondary'

# Add data
```angular2html
with Session(engine) as session:
    session.add(class_table(column="value))
```

# View data
```angular2html
obj = session.query(class_table).all()
```

# Menjalankan Aplikasi
## 1. Membuat dan menjalankan environment
```angular2html
# membuat environment
python -m venv venv
# menjalankan environment
.venv/Scripts/activate
```
## 2. Menjalankan aplikasi
```angular2html
python seed.py
```

## Note
1. back_populates = jabat tangan dua arah: “atribut saya berpasangan dengan atribut itu di kelas sebelah.”
2. secondary = jembatan many-to-many: “lewat tabel ini kita terhubung.”
3. Pakai secondary hanya bila tabel jembatan tanpa kolom tambahan.
4. Jika ada kolom tambahan → gunakan association object (kelas terpisah), bukan secondary.

## Kesalahan Umum
1. back_populates tidak cocok namanya antara dua sisi → relasi tidak sinkron.
2. Mengisi secondary dengan class ORM (salah). secondary harus Table/selectable, bukan mapped class.
3. Mencampur pola secondary dan association object pada tabel yang sama tanpa viewonly/association_proxy → duplikasi/overlap warning.