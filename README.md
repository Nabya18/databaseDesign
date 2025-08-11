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
## Create Virtual Environment
```angular2html
# Create virtual environment
python -m venv venv         #windows
python3 -m venv venv        #mac/linux
# Activate virtual environment
venv\Scripts\activate       #windows
source venv/bin/activate    #mac/linux
```

## Install Dependencies
```angular2html
pip install -r requirements.txt
```

## Run the Program
```angular2html
python seed.py
```

## Notes
1. back_populates = two-way handshake: "my attribute is paired with that attribute in the other class."
2. secondary = many-to-many bridge: "we connect through this table."
3. Use secondary only when the bridge table has no additional columns.
4. If there are additional columns → use association object (separate class), not secondary.

## Common Mistakes
1. back_populates names don't match between two sides → relationship not synchronized.
2. Filling secondary with ORM class (wrong). secondary must be Table/selectable, not mapped class.
3. Mixing secondary pattern and association object on the same table without viewonly/association_proxy → duplication/overlap warning.