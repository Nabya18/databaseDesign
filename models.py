from __future__ import annotations
import datetime
from sqlalchemy import Integer, String, Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# --- Core ---
class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # Relation
    users: Mapped[list["User"]] = relationship(back_populates="country")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    # relation
    country: Mapped["Country"] = relationship(back_populates="users")
    playlists: Mapped[list["Playlist"]] = relationship(back_populates="user")
    billing_history: Mapped[list["BillingHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    listening_history: Mapped[list["ListeningHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    followed_artists: Mapped[list["Artist"]] = relationship(secondary="follows", back_populates="followers")
    liked_songs: Mapped[list["Song"]] = relationship(secondary="song_likes", back_populates="liked_by_users")

class Artist(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    bio: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    # Relation
    albums: Mapped[list["Album"]] = relationship(back_populates="artist")
    songs: Mapped[list["Song"]] = relationship(secondary="song_artists", back_populates="artists")
    followers: Mapped[list["User"]] = relationship(secondary="follows", back_populates="followed_artists")

class Album(Base):
    __tablename__ = "albums"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    release_date: Mapped[datetime.date] = mapped_column(Date)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"))
    cover_image_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    # Relation
    artist: Mapped["Artist"] = relationship(back_populates="albums")
    songs: Mapped[list["Song"]] = relationship(back_populates="album", cascade="all, delete-orphan")

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    songs: Mapped[list["Song"]] = relationship(secondary="song_genres", back_populates="genres")

class Song(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"))
    duration_seconds: Mapped[int] = mapped_column(Integer)
    track_number: Mapped[int] = mapped_column(Integer)
    release_date: Mapped[datetime.date] = mapped_column(Date)
    popularity_score: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    # Relation
    album: Mapped["Album"] = relationship(back_populates="songs")
    listening_history: Mapped[list["ListeningHistory"]] = relationship(back_populates="song", cascade="all, delete-orphan")

    artists: Mapped[list["Artist"]] = relationship(secondary="song_artists", back_populates="songs")
    genres: Mapped[list["Genre"]] = relationship(secondary="song_genres", back_populates="songs")
    liked_by_users: Mapped[list["User"]] = relationship(secondary="song_likes", back_populates="liked_songs")

    playlist_songs: Mapped[list["PlaylistSong"]] = relationship(back_populates="song", cascade="all, delete-orphan")

class Playlist(Base):
    __tablename__ = "playlists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    # Relation
    user: Mapped["User"] = relationship(back_populates="playlists")
    playlist_songs: Mapped[list["PlaylistSong"]] = relationship(back_populates="playlist", cascade="all, delete-orphan")

# --- History / others ---
class BillingHistory(Base):
    __tablename__ = "billing_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    billed_amount: Mapped[int] = mapped_column(Integer)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relation
    user: Mapped["User"] = relationship(back_populates="billing_history")

class ListeningHistory(Base):
    __tablename__ = "listening_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    played_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    device_info: Mapped[str] = mapped_column(String)

    # Relation
    song: Mapped["Song"] = relationship(back_populates="listening_history")
    user: Mapped["User"] = relationship(back_populates="listening_history")

# --- Association tables (PK komposit) ---
class SongArtist(Base):
    __tablename__ = "song_artists"
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), primary_key=True)
    role: Mapped[str | None] = mapped_column(String, nullable=True)

class SongGenre(Base):
    __tablename__ = "song_genres"
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)

class PlaylistSong(Base):
    __tablename__ = "playlist_songs"
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlists.id"), primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    added_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    # Relation
    playlist: Mapped["Playlist"] = relationship(back_populates="playlist_songs")
    song: Mapped["Song"] = relationship(back_populates="playlist_songs")

class SongLike(Base):
    __tablename__ = "song_likes"
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    liked_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

class Follow(Base):
    __tablename__ = "follows"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), primary_key=True)
    followed_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)