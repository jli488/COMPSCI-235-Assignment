from movie.adapters.database_repository import SqlAlchemyRepository
from movie.domainmodel.movie import User


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    repo.add_user(user)
    repo.add_user(User('Martin', '123456789'))
    user2 = repo.get_user('Dave')
    assert user2 == user and user2 is user
