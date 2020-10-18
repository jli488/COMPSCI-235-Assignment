from datetime import datetime
from typing import List

from movie.domainmodel.actor import Actor
from movie.domainmodel.director import Director
from movie.domainmodel.genre import Genre


class User:
    def __init__(self, username: str, password: str):
        self._user_name = username
        self._password = password
        self._watched_movies = list()
        self._review_list = list()
        self._time_spent_watching_movies_minutes = 0

    @property
    def username(self):
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
        return f"<User {self.username}>"

    def __eq__(self, other: 'User') -> bool:
        if type(other) == User:
            return self.username == other.username
        return False

    def __lt__(self, other: 'User'):
        if type(other) == User:
            return self.username < other.username
        else:
            raise TypeError(f'Cannot compare User type with {type(other)}')

    def __hash__(self):
        return hash(self.username)

    def watch_movie(self, movie: 'Movie'):
        if movie not in self.watched_movies:
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: 'Review'):
        if review not in self.reviews:
            self._review_list.append(review)

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }


class Review:
    def __init__(self, movie: 'Movie', user: 'User', review_text: str, rating: int, timestamp: float = None):
        self._movie = movie
        self._user = user
        self._review_text = review_text

        if not timestamp:
            timestamp = datetime.now().timestamp()
        self._timestamp = timestamp

        if 0 < rating < 11:
            self._rating = rating
        else:
            self._rating = None

        self._review_id = str(self.movie.id) + self.username + str(self.timestamp)

    @property
    def id(self) -> str:
        return self._review_id

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def review_text(self) -> str:
        return self._review_text

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def username(self) -> str:
        return self._user.username

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


class Movie:
    def __init__(self, title: str, year: int):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()
        if year >= 1900:
            self._year = year
        else:
            self._year = None

        self._movie_id = str(self.title).lower().replace(" ", "_") + "_" + str(self.year)
        self._description = None
        self._director = None
        self._actors = list()
        self._genres = list()
        self._reviews = list()
        self._runtime_minutes = 0

    def __repr__(self):
        return f"<Movie {self.title}, {self.year}>"

    def __eq__(self, other: 'Movie') -> bool:
        if type(self) == type(other) and \
                self.title.lower() == other.title.lower() and \
                self.year == other.year:
            return True
        return False

    def __lt__(self, other: 'Movie') -> bool:
        if type(self) != type(other):
            raise TypeError(f"Cannot compare Movie instance with {type(other)}")
        else:
            if self.title < other.title:
                return True
            elif self.title > other.title:
                return False
            else:
                return self.year < other.year

    def __hash__(self) -> int:
        return hash((self.title, self.year))

    @property
    def id(self) -> str:
        return self._movie_id

    @property
    def movie_id(self) -> str:
        return self._movie_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        if not (title == "" or type(title) is not str):
            self._title = title.strip()

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, year: int):
        if year >= 1900:
            self._year = year

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        if not (description == "" or type(description) is not str):
            self._description = description.strip()

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, director: Director):
        if type(director) == Director:
            self._director = director

    @property
    def actors(self) -> List[Actor]:
        return self._actors

    @actors.setter
    def actors(self, *actors: Actor):
        for actor in actors:
            assert type(actor) is Actor, \
                f"actor should be type Actor, instead {type(actor)} found"
        self._actors = actors

    @property
    def genres(self) -> List[Genre]:
        return self._genres

    @genres.setter
    def genres(self, genres: List[Genre]):
        for genre in genres:
            assert type(genre) is Genre, \
                f"genre should be type Genre, instead {type(genre)} found"
        self._genres = genres

    @property
    def reviews(self) -> List[Review]:
        return self._reviews

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes: int):
        if runtime_minutes > 0:
            self._runtime_minutes = runtime_minutes
        else:
            raise ValueError("runtime_minutes should be positive")

    def add_actor(self, actor: Actor):
        if type(actor) is Actor:
            self._actors.append(actor)

    def remove_actor(self, actor: Actor):
        for actor_to_remove in self._actors:
            if actor_to_remove == actor:
                self._actors.remove(actor_to_remove)

    def add_genre(self, genre: Genre):
        if type(genre) is Genre:
            self._genres.append(genre)

    def remove_genre(self, genre: Genre):
        for genre_to_remove in self._genres:
            if genre_to_remove == genre:
                self._genres.remove(genre_to_remove)

    def add_review(self, review: Review):
        if type(review) is Review:
            self._reviews.append(review)

    def remove_review(self, review: Review):
        for review_to_remove in self._reviews:
            if review_to_remove == review:
                self._reviews.remove(review_to_remove)

    def remove_review_by_id(self, review_id: str):
        for review_to_remove in self._reviews:
            if review_to_remove.id == review_id:
                self._reviews.remove(review_to_remove)

    def set_director(self, director: Director):
        self._director = director
