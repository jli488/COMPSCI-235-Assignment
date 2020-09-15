import abc

from 


class RepositoryException(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_movie(self, movie: Movie):
