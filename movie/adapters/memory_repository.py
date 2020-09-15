from bisect import insort_left

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.movie import Movie
from movie.utils.movie_reader import MovieFileCSVReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()
        self._movies_index = dict()

    def add_movie(self, movie: Movie) -> None:
        if movie in self._movies:
            return
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, title: str, year: int) -> Movie:
        return next((movie for movie in self._movies
                     if movie.title.lower() == title.lower()
                     and movie.year == year),
                    None)

    def get_number_of_movies(self) -> int:
        return len(self._movies)

    def get_first_movie(self) -> Movie:
        return self._get_movie_by_idx(0)

    def get_last_movie(self) -> Movie:
        return self._get_movie_by_idx(-1)

    def _get_movie_by_idx(self, idx: int) -> Movie:
        try:
            movie = self._movies[idx]
        except IndexError:
            movie = None
        return movie


def populate(data_path: str, repo: MemoryRepository) -> None:
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()
    for movie in reader.dataset_of_movies:
        repo.add_movie(movie)
