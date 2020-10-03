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


def test_find_fuzzy_match():
    items = ['term111', 'term222', 'term333']
    distance_1_item = 'Term222'
    distance_2_item = 'TErm222'
    distance_3_item = 'tm22'
    matched_item = movie_services._find_fuzzy_match(distance_1_item, (i for i in items))
    assert matched_item == 'term222'
    matched_item = movie_services._find_fuzzy_match(distance_2_item, (i for i in items))
    assert matched_item == 'term222'
    matched_item = movie_services._find_fuzzy_match(distance_3_item, (i for i in items))
    assert matched_item == 'term222'


def test_fetch_movie_info_by_id(memory_repo):
    movie_id = 'movie12000'
    movie_info = movie_services.fetch_movie_info_by_id(movie_id, memory_repo)
    assert movie_info['movie_title'] == 'Movie1'


def test_get_n_movies(memory_repo):
    movies = movie_services.get_n_movies(2, 0, memory_repo)
    assert len(movies) == 2
    assert next((i for i in movies if i.title == 'Movie1')) is not None
    assert next((i for i in movies if i.title == 'Movie2')) is not None
    movies = movie_services.get_n_movies(2, 4, memory_repo)
    assert len(movies) == 1
    assert next((i for i in movies if i.title == 'Movie5')) is not None


def test_get_movie_num(memory_repo):
    assert movie_services.get_movie_num(memory_repo) == 5


def test_get_n_movies_by_actor(memory_repo):
    movies, matched_count = movie_services.get_n_movies_by_actor(0, 1, memory_repo, 'Actor2')
    assert len(movies) == 1
    assert matched_count == 2
    movies, matched_count = movie_services.get_n_movies_by_actor(0, 5, memory_repo, 'Actor2')
    assert len(movies) == 2
    assert matched_count == 2


def test_get_n_movies_by_director(memory_repo):
    movies, matched_count = movie_services.get_n_movies_by_director(0, 2, memory_repo, 'Director1')
    assert len(movies) == 2
    assert matched_count == 3
    movies, matched_count = movie_services.get_n_movies_by_director(2, 5, memory_repo, 'Director1')
    assert len(movies) == 1
    assert matched_count == 3


def test_get_n_movies_by_genre(memory_repo):
    movies, matched_count = movie_services.get_n_movies_by_genre(0, 2, memory_repo, 'Genre1')
    assert len(movies) == 2
    assert matched_count == 3
    movies, matched_count = movie_services.get_n_movies_by_genre(2, 5, memory_repo, 'Genre1')
    assert len(movies) == 1
    assert matched_count == 3


def test_get_n_movies_by_director_fuzzy(memory_repo):
    movies, matched_count = movie_services.get_n_movies_by_director_fuzzy(0, 2, memory_repo, 'direcor1')
    assert len(movies) == 2
    assert matched_count == 3
    assert next((i for i in movies if i.title == 'Movie1')) is not None
    assert next((i for i in movies if i.title == 'Movie2')) is not None
    movies, matched_count = movie_services.get_n_movies_by_director_fuzzy(2, 5, memory_repo, 'direcor1')
    assert len(movies) == 1
    assert matched_count == 3
    assert next((i for i in movies if i.title == 'Movie3')) is not None


def test_get_n_movies_by_actor_fuzzy(memory_repo):
    movies, matched_count = movie_services.get_n_movies_by_actor_fuzzy(0, 2, memory_repo, 'acto3')
    assert len(movies) == 2
    assert matched_count == 3
    assert next((i for i in movies if i.title == 'Movie3')) is not None
    assert next((i for i in movies if i.title == 'Movie4')) is not None
    movies, matched_count = movie_services.get_n_movies_by_actor_fuzzy(2, 5, memory_repo, 'acto3')
    assert len(movies) == 1
    assert matched_count == 3
    assert next((i for i in movies if i.title == 'Movie5')) is not None


def test_get_n_movies_by_genre_fuzzy(memory_repo):
    movies, matched_count = movie_services.get_n_movies_by_genre_fuzzy(0, 2, memory_repo, 'genr1')
    assert len(movies) == 2
    assert matched_count == 3
    assert next((i for i in movies if i.title == 'Movie1')) is not None
    assert next((i for i in movies if i.title == 'Movie3')) is not None
    movies, matched_count = movie_services.get_n_movies_by_genre_fuzzy(2, 5, memory_repo, 'genr1')
    assert len(movies) == 1
    assert matched_count == 3
    assert next((i for i in movies if i.title == 'Movie5')) is not None
