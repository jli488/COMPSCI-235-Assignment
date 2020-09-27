from datetime import datetime, timedelta

import pytest

from movie.domainmodel.movie import Movie, Review


@pytest.fixture
def movie():
    return Movie("Moana1", 2016)


@pytest.fixture
def movie2():
    return Movie("Moana2", 2016)


def test_init(movie):
    review_text = "This movie was very enjoyable."
    rating = 8
    timestamp = datetime.now()
    review = Review(movie, review_text, rating, timestamp)
    assert review.movie == movie
    assert review.review_text == review_text
    assert review.rating == rating
    assert review.timestamp == timestamp


def test_init_invalid(movie):
    review_text = "This movie was very enjoyable."
    rating = 11
    timestamp = datetime.now()
    review = Review(movie, review_text, rating, timestamp)
    assert review.movie == movie
    assert review.review_text == review_text
    assert review.rating is None
    assert review.timestamp == timestamp


def test_equal(movie, movie2):
    review_text = "This movie was very enjoyable."
    review_text2 = "This movie was very enjoyable.2"
    rating = 11
    timestamp = datetime.now()
    timestamp2 = datetime.now() + timedelta(seconds=1)
    review = Review(movie, review_text, rating, timestamp)
    review2 = Review(movie, review_text, rating, timestamp)
    assert review == review2
    review3 = Review(movie2, review_text, rating, timestamp)
    assert review != review3
    review4 = Review(movie, review_text, rating, timestamp2)
    assert review != review4
    review5 = Review(movie, review_text2, rating, timestamp)
    assert review != review5
