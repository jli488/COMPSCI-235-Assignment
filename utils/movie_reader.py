import csv
from typing import List

from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie


class MovieFileCSVReader(object):
    def __init__(self, data_path):
        self._data_path = data_path
        self._dataset_of_movies = set()
        self._dataset_of_actors = set()
        self._dataset_of_directors = set()
        self._dataset_of_genres = set()

    @property
    def dataset_of_movies(self) -> List[Movie]:
        return list(self._dataset_of_movies)

    @property
    def dataset_of_actors(self) -> List[Actor]:
        return list(self._dataset_of_actors)

    @property
    def dataset_of_directors(self) -> List[Director]:
        return list(self._dataset_of_directors)

    @property
    def dataset_of_genres(self) -> List[Genre]:
        return list(self._dataset_of_genres)

    def _read_field(self, record: dict, key: str, sep: str) -> List[str]:
        str_objects = record.get(key)
        if str_objects:
            return str_objects.split(sep)
        return []

    def read_csv_file(self):
        with open(self._data_path, mode='r', encoding='utf-8-sig') as f:
            records = csv.DictReader(f)
            for record in records:
                movie = Movie(record.get('Title'), int(record.get('Year', 0)))
                self._dataset_of_movies.add(movie)

                for actor in self._read_field(record, 'Actors', ','):
                    self._dataset_of_actors.add(Actor(actor))

                for genre in self._read_field(record, 'Genre', ','):
                    self._dataset_of_genres.add(Genre(genre))

                for director in self._read_field(record, 'Director', ','):
                    self._dataset_of_directors.add(Director(director))
