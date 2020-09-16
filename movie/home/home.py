from flask import Blueprint, render_template

from movie.utils.helpers import *

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        selected_movies=get_selected_movies()
    )
