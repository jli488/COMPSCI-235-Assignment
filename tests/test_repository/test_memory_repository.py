from movie.domainmodel.movie import Movie


def test_repository_can_add_movie(memory_repo):
    movie = Movie('Test Movie', 2020)
    memory_repo.add_movie(movie)
    assert memory_repo.get_movie('test movie', 2020) is movie
    assert memory_repo.get_total_number_of_movies() == 6


def test_repository_can_get_movie(memory_repo):
    movie = Movie('Test Movie', 2020)
    memory_repo.add_movie(movie)
    assert memory_repo.get_movie('test movie', 2020) is movie


def test_repository_can_not_get_movie(memory_repo):
    assert memory_repo.get_movie('Not Existing Movie', 9999) is None


def test_repository_get_first_movie(memory_repo):
    movie_1 = Movie("Movie1", 2000)
    assert memory_repo.get_first_movie() == movie_1


def test_repository_get_last_movie(memory_repo):
    movie_5 = Movie("Movie5", 2004)
    assert memory_repo.get_last_movie() == movie_5


def test_repository_get_n_movies(memory_repo):
    movie_1 = Movie("Movie1", 2000)
    movie_2 = Movie("Movie2", 2001)
    movies = memory_repo.get_n_movies(2, 0)
    assert len(movies) == 2
    assert movie_1 in movies
    assert movie_2 in movies


def test_repository_get_more_than_n_movies(memory_repo):
    movies = memory_repo.get_n_movies(10, 0)
    assert len(movies) == 5


def test_repository_get_n_movies_with_offset(memory_repo):
    movie_3 = Movie("Movie3", 2002)
    movie_4 = Movie("Movie4", 2003)
    movies = memory_repo.get_n_movies(2, 1)
    assert len(movies) == 2
    assert movie_3 in movies
    assert movie_4 in movies


def test_get_total_numerb_of_movies(memory_repo):
    assert memory_repo.get_total_number_of_movies() == 5


def test_delete_movie(memory_repo):
    movie_3 = Movie("Movie3", 2002)
    res = memory_repo.delete_movie(movie_3)
    assert res is True
    assert memory_repo.get_total_number_of_movies() == 4


def test_delete_not_exist_movie(memory_repo):
    movie_not_exist = Movie('Not Existing Movie', 9999)
    res = memory_repo.delete_movie(movie_not_exist)
    assert res is False
    assert memory_repo.get_total_number_of_movies() == 5
