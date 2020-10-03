import os

import pytest

from movie import create_app
from movie.adapters import memory_repository
from movie.domainmodel.movie import Movie
from movie.domainmodel.user import User
from movie.utils.constants import USER_DATA_FILE, MOVIE_DATA_FILE, REVIEW_DATA_FILE

TEST_CONFIG = {
    'TESTING': True,
    'TEST_MOVIE_DATA_PATH': os.path.join('tests', 'datafiles', MOVIE_DATA_FILE),
    'TEST_REVIEWS_DATA_PATH': os.path.join('tests', 'datafiles', REVIEW_DATA_FILE),
    'TEST_USERS_DATA_PATH': os.path.join('tests', 'datafiles', USER_DATA_FILE),
    'WTF_CSRF_ENABLED': False
}


@pytest.fixture
def memory_repo():
    repo = memory_repository.MemoryRepository()
    movie_1 = Movie("Movie1", 2000)
    movie_2 = Movie("Movie2", 2001)
    movie_3 = Movie("Movie3", 2002)
    movie_4 = Movie("Movie4", 2003)
    movie_5 = Movie("Movie5", 2004)
    repo.add_movie(movie_1)
    repo.add_movie(movie_2)
    repo.add_movie(movie_3)
    repo.add_movie(movie_4)
    repo.add_movie(movie_5)

    user = User(username='ExistUser', password='Password123')
    repo.add_user(user)
    return repo


@pytest.fixture
def client():
    my_app = create_app(TEST_CONFIG)
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_user_001', password='Test123456'):
        return self._client.post(
            'auth/login',
            data={'username': username,
                  'password': password}
        )

    def logout(self):
        return self._client.get('auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
