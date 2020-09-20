from flask import Blueprint, render_template

from movie.authentication.auth_forms import RegistrationForm
from movie.utils.constants import AUTH_BP, REGISTER_ENDPOINT

auth_blueprint = Blueprint(AUTH_BP, __name__)


@auth_blueprint.route('/' + REGISTER_ENDPOINT, methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    unique_username = True

    if form.validate_on_submit():
        pass
