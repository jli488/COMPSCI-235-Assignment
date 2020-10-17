from sqlalchemy.orm import sessionmaker

from movie.adapters.repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory: sessionmaker):
        pass


def populate_movies(database_engine, movie_data_path):
    return None


def populate_users(database_engine, users_data_path):
    return None


def populate_reviews(database_engine, reviews_data_path):
    return None
