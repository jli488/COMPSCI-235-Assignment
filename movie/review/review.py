from flask import Blueprint, request, render_template, url_for, redirect

import movie.adapters.repository as repo

from movie.authentication.authentication import login_required
from movie.domainmodel.movie import Review
from movie.review.review_form import MovieReviewForm
from movie.utils.constants import REVIEW_BP, REVIEW_ENDPOINT

review_blueprint = Blueprint(REVIEW_BP, __name__)


@review_blueprint.route('/' + REVIEW_ENDPOINT, methods=['GET', 'POST'])
@login_required
def add_review():
    form = MovieReviewForm()
    movie_id = request.args.get('movie_id')
    movie = repo.repo_instance.get_movie_by_id(movie_id)
    if movie is None:
        return redirect(url_for('home_bp.home'))

    if form.validate_on_submit():
        rating = int(form.rating.data)
        comment = form.review_text.data
        review = Review(movie, comment, rating)
        movie.add_review(review)
        return render_template(
            'movie/movie_info.html',
            movie=movie,
        )

    return render_template(
        'review/add_review.html',
        form=form,
        movie=movie
    )
