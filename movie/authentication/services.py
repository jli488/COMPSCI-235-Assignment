import csv

from flask import current_app, has_app_context
from werkzeug.security import generate_password_hash, check_password_hash

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.movie import User


class DuplicatedUsernameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    if repo.get_user(username):
        raise DuplicatedUsernameException
    password_hash = generate_password_hash(password)
    new_user = User(username, password_hash)
    repo.add_user(new_user)
    if has_app_context() and (current_app.config['REPOSITORY'] == 'memory'):
        _save_users_to_disk(current_app.config['USER_DATA_PATH'], repo)


def _save_users_to_disk(data_path: str, repo: AbstractRepository) -> None:
    with open(data_path, 'w', newline='') as f:
        user_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for user in repo.users:
            user_writer.writerow([user.username, user.password])


def get_user(username: str, repo: AbstractRepository) -> dict:
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    return user.to_dict()


def authenticate_user(username: str, password: str, repo: AbstractRepository) -> None:
    authenticated = False
    user = repo.get_user(username)
    if user:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException
