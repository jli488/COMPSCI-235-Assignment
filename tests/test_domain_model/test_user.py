import pytest

from movie.domainmodel.movie import User


def test_init():
    user = User('Martin', 'pw12345')
    assert user.username == 'Martin'
    assert user.password == 'pw12345'


def test_eq():
    user1 = User('Martin', 'pw123452')
    user2 = User('Martin', 'pw123451')
    user3 = User('Martain', 'pw123')
    user4 = 'Martin'
    assert user1 == user2
    assert user1 != user3
    assert user1 != user4


def test_lt():
    user1 = User('a', 'pw123452')
    user2 = User('b', 'pw123451')
    assert user1 < user2
    with pytest.raises(TypeError):
        _ = user1 < 'c'
