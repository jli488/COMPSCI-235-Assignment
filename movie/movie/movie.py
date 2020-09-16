from flask import Blueprint, request, render_template, url_for

from movie.movie import services
import movie.adapters.repository as repo

movie_blueprint = Blueprint('movie_bp', __name__)


@movie_blueprint.route('/movies')
def movies():
    movies_per_page = 5
    offset = int(request.args.get('offset', 0))
    movies = services.get_n_articles(movies_per_page, offset, repo.repo_instance)
    total_movies = services.get_article_num(repo.repo_instance)

    prev_url = None
    first_url = None
    next_url = None
    last_url = None

    if offset > 0:
        prev_url = url_for('movie_bp.movies', offset=offset - 1)
        first_url = url_for('movie_bp.movies')
    if offset * movies_per_page + len(movies) < total_movies:
        next_url = url_for('movie_bp.movies', offset=offset + 1)

        if total_movies % movies_per_page == 0:
            last_page = total_movies // movies_per_page - 1
        else:
            last_page = total_movies // movies_per_page
        last_url = url_for('movie_bp.movies', offset=last_page)

    return render_template(
        'movie/movie.html',
        title='Movies',
        movies=movies,
        first_url=first_url,
        last_url=last_url,
        prev_url=prev_url,
        next_url=next_url
    )
