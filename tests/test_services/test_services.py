import pytest

from movie.authentication import services as auth_services
from movie.authentication.services import AuthenticationException
from movie.movie import services as movie_services
from movie.review import services as review_services


def test_can_add_user(memory_repo):
    username = 'TestUser'
    password = 'Password123'
    auth_services.add_user(username, password, memory_repo)
    user_dict = auth_services.get_user(username, memory_repo)
    assert user_dict['username'] == 'TestUser'
    assert user_dict['password'].startswith('pbkdf2:sha256:')

    user_dict = auth_services.get_user(username.lower(), memory_repo)
    assert user_dict['username'] == 'TestUser'
    assert user_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(memory_repo):
    username = 'ExistUser'
    password = 'abcd1A23'

    with pytest.raises(auth_services.DuplicatedUsernameException):
        auth_services.add_user(username, password, memory_repo)

    with pytest.raises(auth_services.DuplicatedUsernameException):
        auth_services.add_user(username.lower(), password, memory_repo)


def test_authentication_with_valid_credentials(memory_repo):
    username = 'TestUser'
    password = 'abcd1A23'

    auth_services.add_user(username, password, memory_repo)

    try:
        auth_services.authenticate_user(username, password, memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(memory_repo):
    username = 'TestUser'
    password = 'abcd1A23'

    auth_services.add_user(username, password, memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(username, '0987654321', memory_repo)


def test_can_add_review(memory_repo):
    movie_id = 'movie12000'
    review_text = 'This is a test review'
    username = 'ExistUser'
    rating = 4
    review_services.add_review(movie_id, username, review_text, rating, memory_repo)
    movie_dict = movie_services.fetch_movie_info_by_id(movie_id, memory_repo)
    assert movie_dict.get('movie_reviews') is not None
    assert next(
        (dictionary['comment']
         for dictionary in movie_dict.get('movie_reviews')
         if dictionary['comment'] == review_text),
        None) is not None


def test_can_remove_review(memory_repo):
    movie_id = 'movie12000'
    review_text = 'ToMakeAUniqueComment8X2g$1)*'
    username = 'ExistUser'
    rating = 4
    review_services.add_review(movie_id, username, review_text, rating, memory_repo)
    movie_dict = movie_services.fetch_movie_info_by_id(movie_id, memory_repo)
    review_id = [dictionary['id']
              for dictionary in movie_dict.get('movie_reviews')
              if dictionary['comment'] == review_text
              if dictionary['username'] == username][0]
    review_services.remove_review(review_id, movie_id, memory_repo)
    movie_dict = movie_services.fetch_movie_info_by_id(movie_id, memory_repo)
    assert next(
        (dictionary['comment']
         for dictionary in movie_dict.get('movie_reviews')
         if dictionary['comment'] == review_text),
        None) is None
