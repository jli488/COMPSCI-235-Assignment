from datetime import datetime

from movie.domainmodel.movie import Movie


class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int, timestamp: datetime = None):
        self._movie = movie
        self._review_text = review_text

        if not timestamp:
            timestamp = datetime.now()
        self._timestamp = timestamp

        if 0 < rating < 11:
            self._rating = rating
        else:
            self._rating = None

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def review_text(self) -> str:
        return self._review_text

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def rating(self) -> int:
        return self._rating

    def __repr__(self) -> str:
        movie_str = repr(self._movie) + "\n"
        review_str = f"Review: {self._review_text}.\nRating: {self._rating}"
        return movie_str + review_str

    def __eq__(self, other: 'Review') -> bool:
        res = []
        if type(other) == Review:
            for attr_k in self.__dict__.keys():
                res.append(self.__dict__[attr_k] == other.__dict__[attr_k])
            return all(res)
        return False
