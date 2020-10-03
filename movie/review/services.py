import csv
import shutil
import tempfile

from flask import current_app, has_app_context

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.movie import Review


def add_review(movie_id: str, username: str, comment: str, rating: int, repo: AbstractRepository) -> None:
    movie = repo.get_movie_by_id(movie_id)
    if movie:
        review = Review(movie, username, comment, rating)
        movie.add_review(review)
        if has_app_context():
            _save_reviews_to_disk(current_app.config['REVIEW_DATA_PATH'], review)


def _save_reviews_to_disk(data_path: str, review: Review) -> None:
    with open(data_path, 'a', newline='') as f:
        review_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        review_writer.writerow([review.id, review.movie.id,
                                review.username, review.rating,
                                review.review_text, review.timestamp])


def remove_review(review_id: str, movie_id: str, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)
    movie.remove_review_by_id(review_id)
    if has_app_context():
        _remove_review_from_disk(current_app.config['REVIEW_DATA_PATH'], review_id)


def _remove_review_from_disk(data_path: str, review_id: str) -> None:
    tmp_out = tempfile.NamedTemporaryFile(mode='w', newline='', delete=False)
    with open(data_path, 'r', newline='') as input, tmp_out:
        input_reviews = csv.reader(input, delimiter=',')
        writer = csv.writer(tmp_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for review in input_reviews:
            if review[0] != review_id:
                writer.writerow(review)
    shutil.move(tmp_out.name, data_path)
