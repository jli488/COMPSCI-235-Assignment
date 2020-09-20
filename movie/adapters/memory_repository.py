import csv
from bisect import insort_left
from typing import List

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.movie import Movie
from movie.domainmodel.user import User
from movie.utils.movie_reader import MovieFileCSVReader
from movie.utils.user_reader import UserFileCSVReader


class MemoryRepository(AbstractRepository):
    user_file_data_path = 'datafiles/RegisteredUsers.csv'

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()

        self._users = list()

    @property
    def movies(self):
        return (movie for movie in self._movies)

    @property
    def users(self):
        return (user for user in self._users)

    def add_movie(self, movie: Movie) -> bool:
        if movie in self._movies:
            return False
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie
        return True

    def get_movie(self, title: str, year: int) -> Movie:
        return next((movie for movie in self._movies
                     if movie.title.lower() == title.lower()
                     and movie.year == year),
                    None)

    def get_n_movies(self, n: int, offset: int = 0) -> List[Movie]:
        return self._movies[n * offset: n * (offset + 1)]

    def get_total_number_of_movies(self) -> int:
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

    def delete_movie(self, movie_to_delete: Movie) -> bool:
        if movie_to_delete in self._movies:
            self._movies.remove(movie_to_delete)
            return True
        return False

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def get_user(self, username: str) -> User:
        return next((user for user in self._users
                     if user.username == username),
                    None)


def populate_movies(data_path: str, repo: MemoryRepository) -> None:
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()
    for movie in reader.dataset_of_movies:
        repo.add_movie(movie)


def populate_users(data_path: str, repo: MemoryRepository) -> None:
    # Read users from files on disk
    reader = UserFileCSVReader(data_path)
    for user in reader.dataset_of_users:
        repo.add_user(user)


def save_users_to_disk(data_path: str, repo: MemoryRepository) -> None:
    # Overwrite the users file every time we save users to disk
    with open(data_path, 'w', newline='') as f:
        user_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for user in repo.users:
            user_writer.writerow([user.username, user.password])
