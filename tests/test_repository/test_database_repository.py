from movie.adapters.database_repository import SqlAlchemyRepository
from movie.domainmodel.movie import User, Movie


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

    number_of_movies = repo.get_total_number_of_movies()
    new_movie_id = number_of_movies + 1
    movie = Movie('MovieTest', 2020)
    repo.add_movie(movie)

    movie_retrieved = repo.get_movie_by_id(movie.movie_id)
    assert movie_retrieved == movie
