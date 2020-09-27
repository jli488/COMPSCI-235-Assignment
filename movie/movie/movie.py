from typing import Tuple, List

from flask import Blueprint, request, render_template, url_for

import movie.adapters.repository as repo
from movie.domainmodel.movie import Movie
from movie.movie import services
from movie.movie.search_forms import MovieSearchForm
from movie.utils.constants import MOVIE_BP, LIST_MOVIE_ENDPOINT

movie_blueprint = Blueprint(MOVIE_BP, __name__)


@movie_blueprint.route('/' + LIST_MOVIE_ENDPOINT, methods=['GET', 'POST'])
def movies():
    movies_per_page = 5
    form = MovieSearchForm()

    search_by = request.args.get('search_by', None)
    search_key = request.args.get('search_key', None)
    clear_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT)

    if form.validate_on_submit() or (search_by and search_key):
        movies, first_url, prev_url, next_url, last_url = parse_movie_search_request(
            movies_per_page, request, form, search_by, search_key)
    else:
        movies, first_url, prev_url, next_url, last_url = parse_movie_list_request(movies_per_page, request)

    return render_template(
        'movie/movie.html',
        form=form,
        title='Movie List',
        movies=movies,
        clear_url=clear_url,
        first_url=first_url,
        last_url=last_url,
        prev_url=prev_url,
        next_url=next_url
    )


def parse_movie_list_request(movies_per_page: int, request: request) -> Tuple[List[Movie], str, str, str, str]:
    prev_url = None
    first_url = None
    next_url = None
    last_url = None

    offset = int(request.args.get('offset', 0))
    movies = services.get_n_movies(movies_per_page, offset, repo.repo_instance)
    total_movies = services.get_movie_num(repo.repo_instance)

    if offset > 0:
        prev_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, offset=offset - movies_per_page)
        first_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT)
    if offset + len(movies) < total_movies:
        next_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, offset=offset + movies_per_page)

        if total_movies % movies_per_page == 0:
            last_page = total_movies // movies_per_page - 1
        else:
            last_page = total_movies // movies_per_page
        last_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, offset=last_page * movies_per_page)

    return movies, first_url, prev_url, next_url, last_url


def parse_movie_search_request(movies_per_page: int, request: request, form: MovieSearchForm,
                               search_by: str, search_key: str) -> Tuple[List[Movie], str, str, str, str]:
    movies = []
    total_movies = 0
    prev_url = None
    first_url = None
    next_url = None
    last_url = None

    offset = int(request.args.get('offset', 0))
    search_by = form.search_by.data or search_by
    search_key = form.search_text.data or search_key
    if search_by == 'Actor':
        movies, total_movies = services.get_n_movies_by_actor(offset, movies_per_page,
                                                              repo.repo_instance, search_key)
    if search_by == 'Director':
        movies, total_movies = services.get_n_movies_by_director(offset, movies_per_page,
                                                                 repo.repo_instance, search_key)
    if search_by == 'Genre':
        movies, total_movies = services.get_n_movies_by_genre(offset, movies_per_page,
                                                              repo.repo_instance, search_key)

    if offset > 0:
        prev_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, offset=offset - movies_per_page,
                           search_by=search_by,
                           search_key=search_key)
        first_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, search_by=search_by, search_key=search_key)
    if offset * movies_per_page + len(movies) < total_movies:
        next_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, offset=offset + movies_per_page,
                           search_by=search_by,
                           search_key=search_key)

        if total_movies % movies_per_page == 0:
            last_page = total_movies // movies_per_page - 1
        else:
            last_page = total_movies // movies_per_page
        last_url = url_for(MOVIE_BP + '.' + LIST_MOVIE_ENDPOINT, offset=last_page * movies_per_page,
                           search_by=search_by, search_key=search_key)

    form.search_by.data = search_by
    form.search_text.data = search_key

    return movies, first_url, prev_url, next_url, last_url
