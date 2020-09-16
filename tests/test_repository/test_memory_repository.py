from movie.domainmodel.movie import Movie


def test_repository_can_add_movie(memory_repo):
    movie = Movie('Test Movie', 2020)
    memory_repo.add_movie(movie)
    assert memory_repo.get_movie('test movie', 2020) is movie
