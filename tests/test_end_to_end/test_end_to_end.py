from html.parser import HTMLParser

import pytest
from flask import session

from movie.utils.constants import REVIEW_ENDPOINT, LIST_MOVIE_ENDPOINT


def test_login(client, auth):
    status_code = client.get('auth/login').status_code
    assert status_code == 200

    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['username'] == 'test_user_001'


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Movie Home' in response.data


def test_login_required_to_review(client):
    response = client.post('/' + REVIEW_ENDPOINT)
    assert response.headers['Location'] == 'http://localhost/auth/login'


class SimpleDeleteHrefParser(HTMLParser):
    delete_url = None

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if 'href' in attr:
                for element in attr:
                    if 'delete' in element:
                        self.delete_url = element


def test_review(client, auth, app):
    # Test add review
    auth.login()
    response = client.get('/review?movie_title=Guardians+of+the+Galaxy&movie_id=guardians_of_the_galaxy_2014')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data

    movie_id = 'guardians_of_the_galaxy_2014'
    response = client.post(
        f'/review?movie_id={movie_id}',
        data={
            'rating': 4,
            'review_text': 'This is a test review'
        }
    )
    assert response.headers['Location'] == f'http://localhost/movie_info?movie_id={movie_id}'

    # Test if review can be retrieved
    response = client.get(f'/movie_info?movie_id={movie_id}')
    assert response.status_code == 200
    assert b'This is a test review' in response.data

    # Test delete review
    response = client.get(f'/movie_info?movie_id={movie_id}')
    assert b'delete' in response.data
    parser = SimpleDeleteHrefParser()
    parser.feed(str(response.data))
    response = client.get(parser.delete_url)
    assert response.status_code == 302

    response = client.get(f'/movie_info?movie_id={movie_id}')
    assert b'This is a test review' not in response.data


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
            ('', '', b'Username is required'),
            ('cj', '', b'Username needs to be at least 3 characters'),
            ('test', '', b'Password is required'),
            ('test', 'test', b'Password requirements:'),
            ('test_user_001', 'Test#6^0', b'Username is not unique, please try another one'),
    )
)
def test_register_with_invalid_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
            ('test_user_001', 'test', b'Password cannot be authenticated, please check your password'),
            ('test_user_002', 'test', b'User cannot be recognized, please check your username')
    )
)
def test_login_with_invalid_input(client, username, password, message):
    response = client.post(
        '/auth/login',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_page_404(client):
    response = client.get('/movie_info?movie_id=-1')
    assert b'The page doesn\'t exist' in response.data


def test_movie_list(client):
    response = client.get('/' + LIST_MOVIE_ENDPOINT)
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data


def test_movie_search(client):
    response = client.get('/' + LIST_MOVIE_ENDPOINT + "?search_by=Director&search_key=James+Gunn")
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data
    assert b'Prometheus' not in response.data
