import csv
from typing import List, Tuple


class ReviewFileCSVReader(object):
    def __init__(self, data_path):
        self._data_path = data_path
        self._reviews = list()

    @property
    def dataset_of_reviews(self) -> List[Tuple]:
        self.read_csv_file()
        return self._reviews

    def read_csv_file(self):
        with open(self._data_path, 'r') as csv_file:
            reviews = csv.reader(csv_file, delimiter=',')
            for review in reviews:
                movie_id = review[1]
                username = review[2]
                rating = review[3]
                comment = review[4]
                timestamp = review[5]
                self._reviews.append((movie_id, username, comment, int(rating), float(timestamp)))
