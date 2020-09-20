from werkzeug.security import generate_password_hash, check_password_hash

from movie.adapters.repository import AbstractRepository
from movie.domainmodel.user import User


class DuplicatedUsernameException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    if repo.get_user(username):
        raise DuplicatedUsernameException
    password_hash = generate_password_hash(password)
    new_user = User(username, password_hash)
    repo.add_user(new_user)
