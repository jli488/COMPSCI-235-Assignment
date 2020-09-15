from movie.domainmodel.movie import Movie
from movie.domainmodel.review import Review


class User:
    def __init__(self, user_name:str, password: str):
        self._user_name = user_name.strip().lower()
        self._password = password
        self._watched_movies = list()
        self._review_list = list()
        self._time_spent_watching_movies_minutes = 0

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._review_list

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    def __repr__(self) -> str:
        return f"<User {self.user_name}>"

    def __eq__(self, other: 'User') -> bool:
        if type(other) == User:
            return self.user_name == other.user_name
        return False

    def __lt__(self, other: 'User'):
        if type(other) == User:
            return self.user_name < other.user_name
        else:
            raise TypeError(f'Cannot compare User type with {type(other)}')

    def __hash__(self):
        return hash(self.user_name)

    def watch_movie(self, movie: Movie):
        if movie not in self.watched_movies:
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if review not in self.reviews:
            self._review_list.append(review)
