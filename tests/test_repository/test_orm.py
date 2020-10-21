import time

import pytest
from sqlalchemy.exc import IntegrityError

from movie.domainmodel.actor import Actor
from movie.domainmodel.genre import Genre
from movie.domainmodel.movie import User, Movie, Review


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("Andrew", "111")
    return user


def make_movie():
    movie = Movie("Guardians of the Galaxy", 2014)
    return movie


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def insert_movie(empty_session):
    empty_session.execute(
        'INSERT INTO movies (id, movie_id, title, year, description, runtime_minutes, director_id) VALUES'
        '(1, "guardians_of_the_galaxy2014", "Guardians of the Galaxy", 2014, '
        '"A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.", '
        '121, 1)')
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def insert_director(empty_session):
    empty_session.execute(
        'INSERT INTO directors (id, full_name) VALUES'
        '(1, "James Gunn", 2014)')
    row = empty_session.execute('SELECT id from directors').fetchone()
    return row[0]


def insert_actors(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO actors (id, full_name) VALUES'
            '(:id, :full_name)', {'id': value[0], 'full_name': value[1]})
    rows = list(empty_session.execute('SELECT id from actors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Action"), ("Adventure"), ("Sci-Fi")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie_genre_associations(empty_session, movie_key, genre_keys):
    stmt = 'INSERT INTO movie_genres (movie_id, genre_id) VALUES (:movie_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'movie_id': movie_key, 'genre_id': genre_key})


def insert_movie_actors_associations(empty_session, movie_key, actor_keys):
    stmt = 'INSERT INTO movie_actors (movie_id, actor_id) VALUES (:movie_id, :actor_id)'
    for actor_key in actor_keys:
        empty_session.execute(stmt, {'movie_id': movie_key, 'actor_id': actor_key})


def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert fetched_movie == expected_movie
    assert movie_key == fetched_movie.id


def test_loading_of_movie_genres(empty_session):
    movie_id = insert_movie(empty_session)
    genre_ids = insert_genres(empty_session)
    insert_movie_genre_associations(empty_session, movie_id, genre_ids)

    movie = empty_session.query(Movie).get(movie_id)
    genres = [empty_session.query(Genre).get(key) for key in genre_ids]

    for genre in genres:
        assert genre in movie.genres


def test_loading_of_movie_actors(empty_session):
    movie_id = insert_movie(empty_session)
    actor_ids = insert_actors(empty_session, [
        (1, "Chris Pratt"), (2, "Vin Diesel"), (3, "Bradley Cooper"), (4, "Zoe Saldana")
    ])
    insert_movie_actors_associations(empty_session, movie_id, actor_ids)

    movie = empty_session.query(Movie).get(movie_id)
    actors = [empty_session.query(Actor).get(key) for key in actor_ids]

    for actor in actors:
        assert actor in movie.actors


def test_saving_reviews(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Movie).all()
    movie = rows[0]
    user = empty_session.query(User).filter(User._user_name == "Andrew").one()

    review_text = "Some comment text."
    review = Review(movie, user, review_text, 5, time.time())
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, movie_id, comments FROM reviews'))

    assert rows == [(user_key, movie_key, review_text)]
