from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import mapper, relationship

from movie.domainmodel.actor import Actor
from movie.domainmodel.director import Director
from movie.domainmodel.genre import Genre
from movie.domainmodel.movie import Movie, Review, User

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(255), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', String(255), primary_key=True),
    Column('title', String(255)),
    Column('year', Integer),
    Column('description', String(255)),
    Column('run_time_minutes', Integer)
)

reviews = Table(
    'reviews', metadata,
    Column('id', String(255), primary_key=True),
    Column('timestamp', Float, nullable=False),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('comments', String(255)),
    Column('rating', Integer)
)


def map_model_to_tables():
    mapper(User, users, properties={
        '_user_name': users.c.username,
        '_password': users.c.password,
        '_time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '_watched_movies': relationship(Movie),
        '_review_list': relationship(Review, backref='_user')
    })
    mapper(Movie, movies, properties={
        'id': movies.c.id,
        '_title': movies.c.title,
        '_year': movies.c.year,
        '_description': movies.c.description,
        '_runtime_minutes': movies.c.run_time_minutes,
        '_director': relationship(Director),
        '_actors': relationship(Actor),
        '_genres': relationship(Genre),
        '_reviews': relationship(Review, backref='_movie')
    })
    mapper(Review, reviews, properties={
        'id': reviews.c.id,
        '_review_text': reviews.c.comments,
        '_rating': reviews.c.rating,
        '_timestamp': reviews.c.timestamp
    })
    mapper(Genre, genres, properties={
        '_genre_name': genres.c.genre_name
    })
    mapper(Director, directors, properties={
        '_name': directors.c.full_name
    })
    mapper(Actor, actors, properties={
        '_name': actors.c.full_name
    })
