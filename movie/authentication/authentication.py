from flask import Blueprint, render_template

from movie.authentication import services
from movie.authentication.auth_forms import RegistrationForm
from movie.utils.constants import AUTH_BP, REGISTER_ENDPOINT
import movie.adapters.repository as repo

auth_blueprint = Blueprint(AUTH_BP, __name__)


@auth_blueprint.route('/' + REGISTER_ENDPOINT, methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    unique_username = True

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
        except services.DuplicatedUsernameException as e:
            unique_username = False

    return render_template(
        'credentials.html',
        title='Movie Register'
    )
