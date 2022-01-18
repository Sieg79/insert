import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://sieg:885522@localhost:5432/py46_hw')
engine
connection = engine.connect()


def artist_add():
    while True:
        name = input('Имя артиста или Q для выхода: ').title()
        if name == 'Q':
            break
        else:
            genres = []
            while True:
                artist_genre = input('жанр артиста или Q для выхода: ').title()
                if artist_genre == 'Q':
                    break
                else:
                    genres.append(artist_genre)
                    exists_genres = connection.execute("""SELECT COUNT(1) FROM genres
                    WHERE genre_name = %s;""", (artist_genre)).fetchall()
                    if exists_genres[0][0] == 0:
                        connection.execute("INSERT INTO genres(genre_name) VALUES(%s);", (artist_genre))
            connection.execute("INSERT INTO artists(artist_name) VALUES(%s);", (name))
            artist_id = connection.execute("""SELECT artist_id FROM artists
                    WHERE artist_name = %s;""", (name)).fetchall()
            for genre in genres:
                genre_id = connection.execute("""SELECT genre_id FROM genres
                                    WHERE genre_name = %s;""", (genre)).fetchall()
                connection.execute("INSERT INTO genres_artists VALUES(%s, %s);", (genre_id[0][0], artist_id[0][0]))
            print('имя добавлено')


def album_add():
    while True:
        album_name = input('Название альбома или Q для выхода: ').title()
        if album_name == 'Q':
            break
        else:
            artists = []
            while True:
                artist_name = input('Имя автора или Q для выхода: ').title()
                if artist_name == 'Q':
                    break
                else:
                    artists.append(artist_name)
            release_year = int(input('год выхода: '))
            connection.execute("""INSERT INTO albums(album_name, release_date)
                                   VALUES(%s, %s);""", (album_name, release_year))
            album_id = connection.execute("""SELECT album_id FROM albums
                                                    WHERE album_name = %s;""", (album_name)).fetchall()
            for artist in artists:
                artist_id = connection.execute("""SELECT artist_id FROM artists
                                        WHERE artist_name = %s;""", (artist)).fetchall()
                connection.execute("INSERT INTO albums_artists VALUES(%s, %s);", (album_id[0][0], artist_id[0][0]))
            while True:
                track_name = input('название трека или Q для выхода: ').title()
                if track_name == 'Q':
                    break
                else:
                    duration = int(input('длительность в секундах: '))
                    connection.execute("""INSERT INTO tracks(track_name, duration, album_id)
                               VALUES(%s, %s, %s);""", (track_name, duration, album_id[0][0]))


def collection_add():
    while True:
        collection_name = input('Название сборника или Q для выхода: ').title()
        if collection_name == 'Q':
            break
        else:
            release_year = int(input('год выхода или Q для выхода: '))
            connection.execute("""INSERT INTO collections(collection_name, release_date)
                                               VALUES(%s, %s);""", (collection_name, release_year))
            collection_id = connection.execute("""SELECT collection_id FROM collections
                                                 WHERE collection_name = %s;""", (collection_name)).fetchall()
            while True:
                track_name = input('название трека или Q для выхода: ').title()
                if track_name == 'Q':
                    break
                else:
                    track_id = connection.execute("""SELECT track_id FROM tracks
                                                         WHERE track_name = %s;""", (track_name)).fetchall()
                    connection.execute("""INSERT INTO collections_tracks(collection_id, track_id)
                                               VALUES(%s, %s);""", (collection_id[0][0], track_id[0][0]))


while True:
    choise = input(' 1 - добавить исполнителя\n 2 - добавить альбом\n 3 - добавить сборник\n Q - выход\n :  ').title()
    if choise == 'Q':
        break
    elif choise == '1':
        artist_add()
    elif choise == '2':
        album_add()
    elif choise == '3':
        collection_add()
print('END')
