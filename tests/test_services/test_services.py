import pytest

from movie.authentication import services as auth_services
from movie.authentication.services import AuthenticationException


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

# def test_can_add_review(memory_repo):
#     article_id = 3
#     comment_text = 'The loonies are stripping the supermarkets bare!'
#     username = 'fmercury'
#
#     # Call the service layer to add the comment.
#     news_services.add_comment(article_id, comment_text, username, memory_repo)
#
#     # Retrieve the comments for the article from the repository.
#     comments_as_dict = news_services.get_comments_for_article(article_id, memory_repo)
#
#     # Check that the comments include a comment with the new comment text.
#     assert next(
#         (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
#         None) is not None
