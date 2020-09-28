import csv
from typing import List

from movie.domainmodel.movie import Review


class ReviewFileCSVReader(object):
    def __init__(self, data_path):
        self._data_path = data_path
        self._reviews = list()

    @property
    def dataset_of_reviews(self) -> List[Review]:
        self.read_csv_file()
        return self._reviews

    def read_csv_file(self):
        with open(self._data_path, 'r') as csv_file:
            reviews = csv.reader(csv_file, delimiter=',')
            for review in reviews:
                movie_id = review[0]
                rating = review[1]
                comment = review[2]
                self._reviews.append((movie_id, int(rating), comment))
