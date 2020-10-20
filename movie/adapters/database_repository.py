from typing import Generator, List

from flask import _app_ctx_stack
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.actor import Actor
from movie.domainmodel.director import Director
from movie.domainmodel.genre import Genre
from movie.domainmodel.movie import User, Movie, Review
from movie.utils.movie_reader import MovieFileCSVReader
from movie.utils.review_reader import ReviewFileCSVReader
from movie.utils.user_reader import UserFileCSVReader

genres_records = dict()
actors_records = dict()
directors_records = dict()
movie_id_mapping = dict()
user_id_mapping = dict()


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        pass

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    @property
    def movies(self) -> Generator[Movie, None, None]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).order_by(Movie._title).all()
        except NoResultFound:
            pass
        return (movie for movie in movies)

    @property
    def users(self) -> Generator[User, None, None]:
        users = None
        try:
            users = self._session_cm.session.query(User).all()
        except NoResultFound:
            pass
        return (user for user in users)

    @property
    def genres(self) -> Generator[str, None, None]:
        genres = None
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return (genre.genre_name for genre in genres)

    @property
    def actors(self) -> Generator[str, None, None]:
        actors = None
        try:
            actors = self._session_cm.session.query(Actor).all()
        except NoResultFound:
            pass
        return (actor.actor_full_name for actor in actors)

    @property
    def directors(self) -> Generator[str, None, None]:
        directors = None
        try:
            directors = self._session_cm.session.query(Director).all()
        except NoResultFound:
            pass
        return (director.director_full_name for director in directors)

    def add_movie(self, movie: Movie) -> None:
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, title: str, year: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(
                ((Movie._title == title) & (Movie._year == year))).one()
        except NoResultFound:
            pass
        return movie

    def get_movie_by_id(self, movie_id: str) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(
                ((Movie.id == int(movie_id)))).one()
        except NoResultFound:
            pass
        return movie

    def get_n_movies(self, n: int, offset: int) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session\
                .query(Movie)\
                .order_by(Movie._title)\
                .offset(offset)\
                .limit(n).all()
        except NoResultFound:
            pass
        return movies

    def get_total_number_of_movies(self) -> int:
        count = self._session_cm.session.query(Movie).count()
        return count

    def get_first_movie(self) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session\
                .query(Movie)\
                .order_by(Movie._title)\
                .first()
        except NoResultFound:
            pass
        return movie

    def get_last_movie(self) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session\
                .query(Movie)\
                .order_by(desc(Movie._title))\
                .first()
        except NoResultFound:
            pass
        return movie

    def get_movies_by_actor(self, actor: str) -> Generator[Movie, None, None]:
        movies = self._session_cm.session.query(Movie).filter(
            Movie._actors.any(Actor._name == actor)
        ).order_by(Movie._title).all()
        return movies

    def get_movies_by_director(self, director: str) -> Generator[Movie, None, None]:
        movies = self._session_cm.session.query(Movie).filter(
            Movie._director.has(Director._name == director)
        ).order_by(Movie._title).all()
        return movies

    def get_movies_by_genre(self, genre: str) -> Generator[Movie, None, None]:
        movies = self._session_cm.session.query(Movie).filter(
            Movie._genres.any(Genre._genre_name == genre)
        ).order_by(Movie._title).all()
        return movies

    def delete_movie(self, movie_to_delete: Movie) -> bool:
        with self._session_cm as scm:
            scm.session.delete(movie_to_delete)
            scm.commit()

    def add_user(self, user: User) -> None:
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_user_name=username).one()
        except NoResultFound:
            pass
        return user

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def remove_review(self, movie: Movie, review_id: str):
        with self._session_cm as scm:
            try:
                reviews = scm.session.query(Review).filter_by(_review_id=review_id).all()
                if reviews:
                    for review in reviews:
                        scm.session.delete(review)
                scm.commit()
            except NoResultFound:
                pass


def movies_generator(reader: MovieFileCSVReader):
    movie_idx = 0
    for movie in reader.dataset_of_movies:
        movie_idx = movie_idx + 1
        genres = movie.genres
        actors = movie.actors
        director = movie.director

        for genre in genres:
            genre_name = genre.genre_name
            if genre_name not in genres_records:
                genres_records[genre_name] = list()
            genres_records[genre_name].append(movie_idx)

        for actor in actors:
            actor_name = actor.actor_full_name
            if actor_name not in actors_records:
                actors_records[actor_name] = list()
            actors_records[actor_name].append(movie_idx)

        director_name = director.director_full_name
        director_idx = directors_records[director_name]

        # For populating review (map movie id from memory repo to database repo)
        movie_id_mapping[movie.movie_id] = movie_idx

        yield movie_idx, movie.movie_id, movie.title, movie.year, movie.description, movie.runtime_minutes, director_idx


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


def director_generator(reader: MovieFileCSVReader):
    records = list()
    director_key = 0
    for movie in reader.dataset_of_movies:
        director_key += 1
        director_name = movie.director.director_full_name
        directors_records[director_name] = director_key

    for director_name, director_key in directors_records.items():
        records.append((director_key, director_name))
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


def user_generator(reader: UserFileCSVReader):
    user_idx = 0
    for user in reader.dataset_of_users:
        user_idx += 1
        user_id_mapping[user.username] = user_idx
        yield user_idx, user.username, user.password, user.time_spent_watching_movies_minutes


def review_generator(reader: ReviewFileCSVReader):
    review_idx = 0
    for review_fields in reader.dataset_of_reviews:
        review_idx += 1
        movie_id = review_fields.get('movie_id')
        user_name = review_fields.get('username')
        rating = review_fields.get('rating')
        comment = review_fields.get('comment')
        timestamp = review_fields.get('timestamp')
        review_id = review_fields.get('review_id')

        mapped_user_id = user_id_mapping[user_name]
        mapped_movie_id = movie_id_mapping[movie_id]

        yield review_idx, review_id, timestamp, mapped_user_id, mapped_movie_id, comment, rating


def populate_movies(database_engine, movie_data_path):
    global genres_records
    global actors_records
    global directors_records
    global movie_id_mapping

    reader = MovieFileCSVReader(movie_data_path)
    reader.read_csv_file()

    conn = database_engine.raw_connection()
    cursor = conn.cursor()

    insert_directors = """INSERT INTO directors (id, full_name) VALUES (?, ?)"""
    cursor.executemany(insert_directors, director_generator(reader))

    insert_movies = """INSERT INTO movies (id, movie_id, title, year, description, runtime_minutes, director_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movies_generator(reader))

    insert_actors = """INSERT INTO actors (id, full_name) VALUES (?, ?)"""
    cursor.executemany(insert_actors, actor_generator())

    insert_genres = """INSERT INTO genres (id, genre_name) VALUES (?, ?)"""
    cursor.executemany(insert_genres, genre_generator())

    insert_movie_genres = """INSERT INTO movie_genres (id, movie_id, genre_id) VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_movie_actors = """INSERT INTO movie_actors (id, movie_id, actor_id) VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

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

    insert_reviews = """INSERT INTO reviews (id, review_id, timestamp, user_id, movie_id, comments, rating) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, review_generator(reader))

    conn.commit()
    conn.close()
