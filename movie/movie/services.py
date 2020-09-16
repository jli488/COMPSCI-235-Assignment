from typing import List

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.movie import Movie


def get_n_articles(n: int, offset: int, repo: AbstractRepository) -> List[Movie]:
    return repo.get_n_movies(n, offset)


def get_article_num(repo: AbstractRepository) -> int:
    return repo.get_number_of_movies()
