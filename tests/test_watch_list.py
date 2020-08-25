import pytest

from domainmodel.movie import Movie
from domainmodel.watch_list import WatchList


@pytest.fixture
def watch_list():
    return WatchList()


def test_add_movie(watch_list):
    assert watch_list.size() == 0
    watch_list.add_movie(Movie("Moana", 2016))
    watch_list.add_movie(Movie("Ice Age", 2002))
    watch_list.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watch_list.size() == 3
    watch_list.add_movie(Movie("Ice Age", 2002))
    assert watch_list.size() == 3


def test_remove_movie(watch_list):
    watch_list.add_movie(Movie("Moana", 2016))
    watch_list.add_movie(Movie("Ice Age", 2002))
    watch_list.add_movie(Movie("Guardians of the Galaxy", 2012))
    watch_list.remove_movie(Movie("Moana", 2016))
    assert watch_list.size() == 2
    watch_list.remove_movie(Movie("Moana", 2017))
    assert watch_list.size() == 2


def test_select_movie_to_watch(watch_list):
    watch_list.add_movie(Movie("Moana", 2016))
    watch_list.add_movie(Movie("Ice Age", 2002))
    watch_list.add_movie(Movie("Guardians of the Galaxy", 2012))
    movie_to_watch = watch_list.select_movie_to_watch(1)
    assert movie_to_watch == Movie("Ice Age", 2002)
    movie_to_watch = watch_list.select_movie_to_watch(-3)
    assert movie_to_watch == Movie("Moana", 2016)
    movie_to_watch = watch_list.select_movie_to_watch(3)
    assert movie_to_watch is None


def test_size(watch_list):
    assert watch_list.size() == 0
    watch_list.remove_movie(Movie("Moana", 2016))
    assert watch_list.size() == 0
    watch_list.add_movie(Movie("Moana", 2016))
    assert watch_list.size() == 1
    watch_list.remove_movie(Movie("Moana", 2017))
    assert watch_list.size() == 1
    watch_list.remove_movie(Movie("Moana", 2016))
    assert watch_list.size() == 0


def test_iteration(watch_list):
    watch_list.add_movie(Movie("Moana", 2016))
    watch_list.add_movie(Movie("Ice Age", 2002))
    watch_list.add_movie(Movie("Guardians of the Galaxy", 2012))
    res = []
    for movie in watch_list:
        res.append(movie)
    for i in range(len(res)):
        assert res[i] == watch_list.select_movie_to_watch(i)
