import os

from flask import Flask

import movie.adapters.repository as repo
from movie.adapters.memory_repository import MemoryRepository, populate_movies, populate_users


def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    movie_data_path = os.path.join('datafiles', 'Data1000Movies.csv')
    users_data_path = os.path.join('datafiles', 'RegisteredUsers.csv')

    if test_config:
        app.config.from_mapping(test_config)
        movie_data_path = app.config['TEST_MOVIE_DATA_PATH']
        users_data_path = app.config['TEST_USERS_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    populate_movies(movie_data_path, repo.repo_instance)
    populate_users(users_data_path, repo.repo_instance)

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
