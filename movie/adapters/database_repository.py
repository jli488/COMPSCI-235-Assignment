from sqlalchemy.orm import sessionmaker

from movie.adapters.repository import AbstractRepository
from movie.utils.movie_reader import MovieFileCSVReader
from movie.utils.review_reader import ReviewFileCSVReader
from movie.utils.user_reader import UserFileCSVReader

genres_records = dict()
actors_records = dict()
directors_records = dict()
movie_id_mapping = dict()
user_id_mapping = dict()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory: sessionmaker):
        pass


def movies_generator(reader: MovieFileCSVReader):
    for idx, movie in zip(reader.dataset_of_movie_indices,
                          reader.dataset_of_movies):
        genres = movie.genres
        actors = movie.actors
        director = movie.director

        for genre in genres:
            genre_name = genre.genre_name
            if genre_name not in genres_records:
                genres_records[genre_name] = list()
            genres_records[genre_name].append(idx)

        for actor in actors:
            actor_name = actor.actor_full_name
            if actor_name not in actors_records:
                actors_records[actor_name] = list()
            actors_records[actor_name].append(idx)

        director_name = director.director_full_name
        if director_name not in directors_records:
            directors_records[director_name] = list()
        directors_records[director_name].append(idx)

        # For populating review (map movie id from memory repo to database repo)
        movie_id_mapping[movie.movie_id] = idx

        yield idx, movie.title, movie.year, movie.description, movie.runtime_minutes


def genre_generator():
    records = list()
    genre_key = 0

    for genre in genres_records.keys():
        genre_key = genre_key + 1
        records.append((genre_key, genre))
    return records


def actor_generator():
    records = list()
    actor_key = 0

    for actor in actors_records.keys():
        actor_key = actor_key + 1
        records.append((actor_key, actor))
    return records


def director_generator():
    records = list()
    director_key = 0

    for director in directors_records.keys():
        director_key = director_key + 1
        records.append((director_key, director))
    return records


def movie_genres_generator():
    movie_genre_key = 0
    genre_key = 0

    for genre in genres_records.keys():
        genre_key = genre_key + 1
        for movie_key in genres_records[genre]:
            movie_genre_key = movie_genre_key + 1
            yield movie_genre_key, movie_key, genre_key


def movie_actors_generator():
    movie_actor_key = 0
    actor_key = 0

    for actor in actors_records.keys():
        actor_key = actor_key + 1
        for movie_key in actors_records[actor]:
            movie_actor_key = movie_actor_key + 1
            yield movie_actor_key, movie_key, actor_key


def movie_directors_generator():
    movie_director_key = 0
    director_key = 0

    for director in directors_records.keys():
        director_key = director_key + 1
        for movie_key in directors_records[director]:
            movie_director_key = movie_director_key + 1
            yield movie_director_key, movie_key, director_key


def user_generator(reader: UserFileCSVReader):
    records = list()
    user_idx = 0
    for user in reader.dataset_of_users:
        user_idx += 1
        user_id_mapping[user.username] = user_idx
        records.append((user_idx, user.username, user.password, user.time_spent_watching_movies_minutes))
    return records


def review_generator(reader: ReviewFileCSVReader):
    review_idx = 0
    for review_fields in reader.dataset_of_reviews:
        review_idx += 1
        movie_id = review_fields.get('movie_id')
        user_name = review_fields.get('username')
        rating = review_fields.get('rating')
        comment = review_fields.get('comment')
        timestamp = review_fields.get('timestamp')

        mapped_user_id = user_id_mapping[user_name]
        mapped_movie_id = movie_id_mapping[movie_id]

        yield review_idx, timestamp, mapped_user_id, mapped_movie_id, comment, rating


def populate_movies(database_engine, movie_data_path):
    global genres_records
    global actors_records
    global directors_records
    global movie_id_mapping

    reader = MovieFileCSVReader(movie_data_path)
    reader.read_csv_file()

    conn = database_engine.raw_connection()
    cursor = conn.cursor()

    insert_movies = """INSERT INTO movies (id, title, year, description, runtime_minutes) VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movies_generator(reader))

    insert_genres = """INSERT INTO genres (id, genre_name) VALUES (?, ?)"""
    cursor.executemany(insert_genres, genre_generator())

    insert_movie_genres = """INSERT INTO movie_genres (id, movie_id, genre_id) VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_actors = """INSERT INTO actors (id, full_name) VALUES (?, ?)"""
    cursor.executemany(insert_actors, actor_generator())

    insert_movie_actors = """INSERT INTO movie_actors (id, movie_id, actor_id) VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    insert_directors = """INSERT INTO directors (id, full_name) VALUES (?, ?)"""
    cursor.executemany(insert_directors, director_generator())

    insert_movie_directors = """INSERT INTO movie_directors (id, movie_id, director_id) VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_directors, movie_directors_generator())

    conn.commit()
    conn.close()


def populate_users(database_engine, users_data_path):
    global user_id_mapping

    reader = UserFileCSVReader(users_data_path)

    conn = database_engine.raw_connection()
    cursor = conn.cursor()

    insert_users = """INSERT INTO users (id, username, password, time_spent_watching_movies_minutes) VALUES (?, ?, ?, ?)"""
    records = user_generator(reader)
    cursor.executemany(insert_users, records)

    conn.commit()
    conn.close()


def populate_reviews(database_engine, reviews_data_path):
    global user_id_mapping
    global movie_id_mapping

    reader = ReviewFileCSVReader(reviews_data_path)

    conn = database_engine.raw_connection()
    cursor = conn.cursor()

    insert_reviews = """INSERT INTO reviews (id, timestamp, user_id, movie_id, comments, rating) VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, review_generator(reader))

    conn.commit()
    conn.close()
