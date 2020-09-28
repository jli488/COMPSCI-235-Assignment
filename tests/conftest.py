import pytest

from movie.adapters import memory_repository
from movie.domainmodel.movie import Movie

TEST_CONFIG = {
    'TESTING': True,
    'TEST_MOVIE_DATA_PATH': '',
    'TEST_USERS_DATA_PATH': '',
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
    return repo
