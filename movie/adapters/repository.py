import abc
from typing import List

from movie.domainmodel.movie import Movie


repo_instance: 'AbstractRepository' = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_movie(self, movie: Movie) -> None:
        """" Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_n_movies(self, n: int, offset: int) -> List[Movie]:
        """ Get next n Movies from the repository starts from offset. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str, year: int) -> Movie:
        """ Get a Movie from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Get the total number of Movies in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Get the first Movie in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Get the last Movie in the repo. """
        raise NotImplementedError
