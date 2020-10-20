import time

from movie.adapters.database_repository import SqlAlchemyRepository
from movie.domainmodel.movie import User, Movie, Review


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    repo.add_user(user)
    repo.add_user(User('Martin', '123456789'))
    user2 = repo.get_user('Dave')
    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('test_user_001')
    assert user == User('test_user_001', 'Test123456')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_article_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_movies = repo.get_total_number_of_movies()
    assert number_of_movies == 4


def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = Movie('MovieTest', 2020)
    repo.add_movie(movie)
    movie_retrieved = repo.get_movie_by_id(movie.movie_id)
    assert movie_retrieved == movie


def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie('Guardians of the Galaxy', 2014)
    user = repo.get_user('test_user_001')
    review = Review(movie, user, 'Test Review', 5, time.time())
    repo.add_review(review)
    movie2 = repo.get_movie('Guardians of the Galaxy', 2014)
    assert review in movie2.reviews


def test_repository_does_not_retrieve_a_non_existent_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_id('999')
    assert movie is None


def test_repository_can_retrieve_movies_by_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = list(repo.get_movies_by_actor('Vin Diesel'))
    assert len(movies) == 1
    movie = repo.get_movie('Guardians of the Galaxy', 2014)
    assert movie in movies


def test_repository_can_get_first_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_last_movie()
    assert movie.title == 'Split'


def test_repository_can_get_movie_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = Movie('MovieTest', 2020)
    repo.add_movie(movie)
    movie2 = repo.get_movie_by_id(movie.movie_id)
    assert movie == movie2


def test_repository_does_not_retrieve_movie_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movie_by_id('NOT_EXISTS')
    assert movies is None


def test_get_n_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = list(repo.get_n_movies(2, 1))
    assert len(movies) == 2
    titles = [m.title for m in movies]
    assert 'Prometheus' in titles
    assert 'Sing' in titles


def test_get_movie_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = 'Sci-Fi'
    movies = list(repo.get_movies_by_genre(genre))
    titles = [m.title for m in movies]
    assert 'Prometheus' in titles


def test_get_movie_by_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    director = 'James Gunn'
    movies = list(repo.get_movies_by_director(director))
    titles = [m.title for m in movies]
    assert 'Guardians of the Galaxy' in titles


def test_can_delete_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie('Guardians of the Galaxy', 2014)
    assert repo.delete_movie(movie)
    movie = repo.get_movie('Guardians of the Galaxy', 2014)
    assert movie is None

