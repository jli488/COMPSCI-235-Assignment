import os

from flask import Flask

import movie.adapters.repository as repo
from movie.adapters.memory_repository import MemoryRepository, populate_movies, populate_users, populate_reviews
from movie.utils.constants import USER_DATA_FILE, MOVIE_DATA_FILE, REVIEW_DATA_FILE


def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['MOVIE_DATA_PATH'] = os.path.join('movie', 'adapters', 'datafiles', MOVIE_DATA_FILE)
    app.config['USER_DATA_PATH'] = os.path.join('movie', 'adapters', 'datafiles', USER_DATA_FILE)
    app.config['REVIEW_DATA_PATH'] = os.path.join('movie', 'adapters', 'datafiles', REVIEW_DATA_FILE)

    if test_config:
        app.config.from_mapping(test_config)
        app.config['MOVIE_DATA_PATH'] = app.config['TEST_MOVIE_DATA_PATH']
        app.config['MOVIE_DATA_PATH'] = app.config['TEST_USERS_DATA_PATH']
        app.config['REVIEW_DATA_PATH'] = app.config['TEST_REVIEWS_DATA_PATH']

    movie_data_path = app.config['MOVIE_DATA_PATH']
    users_data_path = app.config['USER_DATA_PATH']
    reviews_data_path = app.config['REVIEW_DATA_PATH']
    repo.repo_instance = MemoryRepository()
    populate_movies(movie_data_path, repo.repo_instance)
    populate_users(users_data_path, repo.repo_instance)
    populate_reviews(reviews_data_path, repo.repo_instance)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movie import movie
        app.register_blueprint(movie.movie_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.auth_blueprint)

        from .review import review
        app.register_blueprint(review.review_blueprint)

    return app
