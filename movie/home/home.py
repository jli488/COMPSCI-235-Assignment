from flask import Blueprint, render_template

from movie.utils.constants import HOME_BP

home_blueprint = Blueprint(HOME_BP, __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html'
    )
