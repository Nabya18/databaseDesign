from __future__ import annotations
import datetime
from db import SessionLocal, init_db
from models import (
    Country, User, Genre, Artist, Album, Song,
    Playlist, PlaylistSong, BillingHistory, ListeningHistory
)

def run_seed(drop_and_recreate: bool = True) -> None:
    init_db(drop=drop_and_recreate)
    with SessionLocal() as session:
        # Countries
        idn = Country(name="Indonesia")
        usa = Country(name="USA")
        uk  = Country(name="UK")
        session.add_all([idn, usa, uk])

        # Users
        u1 = User(username="budi_s", email="budi@example.com", password="pwd", is_premium=True, country=idn)
        u2 = User(username="jane_d", email="jane@example.com", password="pwd", country=usa)
        u3 = User(username="citra_k", email="citra@example.com", password="pwd", country=idn)
        session.add_all([u1, u2, u3])

        # Billing (u1)
        session.add_all([
            BillingHistory(user=u1, billed_amount=50000, due_date=datetime.datetime(2025, 9, 1), is_paid=True),
            BillingHistory(user=u1, billed_amount=50000, due_date=datetime.datetime(2025, 10, 1), is_paid=False),
        ])

        # Genres
        pop = Genre(name="Pop"); rock = Genre(name="Rock"); jazz = Genre(name="Jazz")
        folk = Genre(name="Folk"); indie = Genre(name="Indie")
        session.add_all([pop, rock, jazz, folk, indie])

        # Artists
        tulus  = Artist(name="Tulus", bio="An Indonesian singer and songwriter.")
        taylor = Artist(name="Taylor Swift", bio="An American pop and country music superstar.")
        queen  = Artist(name="Queen", bio="A legendary British rock band.")
        session.add_all([tulus, taylor, queen])

        # Albums
        manusia = Album(title="Manusia", release_date=datetime.date(2022, 3, 3), artist=tulus,  cover_image_url="/img/manusia.jpg")
        a1989   = Album(title="1989",    release_date=datetime.date(2014,10,27), artist=taylor, cover_image_url="/img/1989.jpg")
        opera   = Album(title="A Night at the Opera", release_date=datetime.date(1975,11,21), artist=queen, cover_image_url="/img/opera.jpg")
        session.add_all([manusia, a1989, opera])

        # Songs
        hati   = Song(title="Hati-Hati di Jalan", album=manusia, duration_seconds=242, track_number=7,  release_date=manusia.release_date, popularity_score=95)
        inter  = Song(title="Interaksi",          album=manusia, duration_seconds=176, track_number=2,  release_date=manusia.release_date, popularity_score=90)
        blank  = Song(title="Blank Space",        album=a1989,   duration_seconds=231, track_number=2,  release_date=a1989.release_date,   popularity_score=98)
        style  = Song(title="Style",              album=a1989,   duration_seconds=231, track_number=3,  release_date=a1989.release_date,   popularity_score=96)
        bohem  = Song(title="Bohemian Rhapsody",  album=opera,   duration_seconds=355, track_number=11, release_date=opera.release_date,   popularity_score=100)

        # Link songs ↔ artists/genres
        hati.artists.append(tulus); hati.genres.extend([pop, indie])
        inter.artists.append(tulus); inter.genres.extend([pop, indie])
        blank.artists.append(taylor); blank.genres.append(pop)
        style.artists.append(taylor); style.genres.append(pop)
        bohem.artists.append(queen);  bohem.genres.append(rock)
        session.add_all([hati, inter, blank, style, bohem])

        # Likes & follows
        u1.liked_songs.extend([hati, bohem]); u1.followed_artists.extend([tulus, queen])
        u2.liked_songs.extend([blank, style, bohem]); u2.followed_artists.append(taylor)
        u3.liked_songs.append(inter); u3.followed_artists.append(tulus)

        # Listening history
        session.add_all([
            ListeningHistory(user=u1, song=hati,  device_info="iPhone 15"),
            ListeningHistory(user=u2, song=blank, device_info="Android Chrome"),
            ListeningHistory(user=u2, song=blank, device_info="Android Chrome",
                             played_at=datetime.datetime.now() - datetime.timedelta(minutes=10)),
            ListeningHistory(user=u1, song=bohem, device_info="Desktop App"),
        ])

        # Playlists (+ association rows)
        pl1 = Playlist(name="Lagu Santai", description="Teman kerja dan santai", user=u1, is_public=True)
        pl2 = Playlist(name="Top Hits", description="Hits terkini", user=u2, is_public=False)
        session.add_all([pl1, pl2])

        session.add_all([
            PlaylistSong(playlist=pl1, song=hati,  position=1),
            PlaylistSong(playlist=pl1, song=inter, position=2),
            PlaylistSong(playlist=pl2, song=blank, position=1),
            PlaylistSong(playlist=pl2, song=style, position=2),
            PlaylistSong(playlist=pl2, song=bohem, position=3),
        ])

        session.commit()

if __name__ == "__main__":
    run_seed(drop_and_recreate=True)
    print("Database 'spotify.db' created & seeded. ✅")
