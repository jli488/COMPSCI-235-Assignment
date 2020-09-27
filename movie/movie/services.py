from itertools import islice
from typing import List, Generator, Tuple

import editdistance

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.movie import Movie


def get_n_movies(n: int, offset: int, repo: AbstractRepository) -> List[Movie]:
    return repo.get_n_movies(n, offset)


def get_movie_num(repo: AbstractRepository) -> int:
    return repo.get_total_number_of_movies()


def get_n_movies_by_actor(offset: int, n: int, repo: AbstractRepository, actor: str) -> Tuple[List[Movie], int]:
    movies_gen = repo.get_movies_by_actor(actor)
    movies_count = sum(1 for _ in repo.get_movies_by_actor(actor))
    return _get_items_from_offset(offset, n, movies_gen), movies_count


def get_n_movies_by_director(offset: int, n: int, repo: AbstractRepository, director: str) -> Tuple[List[Movie], int]:
    movies_gen = repo.get_movies_by_director(director)
    movies_count = sum(1 for _ in repo.get_movies_by_director(director))
    return _get_items_from_offset(offset, n, movies_gen), movies_count


def get_n_movies_by_genre(offset: int, n: int, repo: AbstractRepository, genre: str) -> Tuple[List[Movie], int]:
    movies_gen = repo.get_movies_by_genre(genre)
    movies_count = sum(1 for _ in repo.get_movies_by_genre(genre))
    return _get_items_from_offset(offset, n, movies_gen), movies_count


def _get_items_from_offset(offset: int, n: int, gen: Generator) -> List:
    items = list(islice(gen, offset, offset + n))
    return items


def get_n_movies_by_director_fuzzy(offset: int, n: int, repo: AbstractRepository,
                                   director_fuzzy: str) -> Tuple[List[Movie], int]:
    director = None
    repo_directors = repo.directors
    director_distances = [(director,
                           editdistance.eval(director.lower(), director_fuzzy.lower()))
                          for director in repo_directors]
    if director_distances:
        director_distances.sort(key=lambda x: x[1])
        director = director_distances[0][0]

    return get_n_movies_by_director(offset, n, repo, director)


def get_n_movies_by_actor_fuzzy(offset: int, n: int, repo: AbstractRepository,
                                actor_fuzzy: str) -> Tuple[List[Movie], int]:
    actor = None
    repo_actor = repo.actors
    actor_distances = [(actor,
                        editdistance.eval(actor.lower(), actor_fuzzy.lower()))
                       for actor in repo_actor]
    if actor_distances:
        actor_distances.sort(key=lambda x: x[1])
        actor = actor_distances[0][0]

    return get_n_movies_by_actor(offset, n, repo, actor)


def get_n_movies_by_genre_fuzzy(offset: int, n: int, repo: AbstractRepository,
                                genre_fuzzy: str) -> Tuple[List[Movie], int]:
    genre = None
    repo_genres = repo.genres
    genre_distances = [(genre,
                        editdistance.eval(genre.lower(), genre_fuzzy.lower()))
                       for genre in repo_genres]
    if genre_distances:
        genre_distances.sort(key=lambda x: x[1])
        genre = genre_distances[0][0]

    return get_n_movies_by_genre(offset, n, repo, genre)
