from flask import Blueprint, render_template, url_for, redirect, session

from movie.authentication import services
from movie.authentication.auth_forms import RegistrationForm, LoginForm
from movie.utils.constants import AUTH_BP, REGISTER_ENDPOINT, LOGIN_ENDPOINT, HOME_BP
import movie.adapters.repository as repo

from movie.adapters.memory_repository import save_users_to_disk

auth_blueprint = Blueprint(AUTH_BP, __name__, url_prefix='/auth')


@auth_blueprint.route('/' + REGISTER_ENDPOINT, methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_error_msg = None
    password_error_msg = None

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
            save_users_to_disk('datafiles/RegisteredUsers.csv', repo.repo_instance)
            return redirect(url_for(AUTH_BP + '.' + LOGIN_ENDPOINT))
        except services.DuplicatedUsernameException as e:
            username_error_msg = 'Username is not unique, please try another one'

    for error in form.password.errors:
        print(error)

    return render_template(
        'credentials.html',
        title='Movie Register',
        form=form,
        username_error_msg=username_error_msg,
        password_error_msg=password_error_msg,
        handler_url=url_for(AUTH_BP + '.' + REGISTER_ENDPOINT)
    )


@auth_blueprint.route('/' + LOGIN_ENDPOINT, methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error_msg = None
    password_error_msg = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repo_instance)
            services.authenticate_user(form.username.data, form.password.data, repo.repo_instance)

            session.clear()
            session['username'] = user['username']
            return redirect(url_for(HOME_BP + '.' + 'home'))
        except services.UnknownUserException:
            username_error_msg = 'User cannot be recognized, please check your username'
        except services.AuthenticationException:
            password_error_msg = 'Password cannot be authenticated, please check your password'

    return render_template(
        'credentials.html',
        title='Movie Login',
        form=form,
        username_error_msg=username_error_msg,
        password_error_msg=password_error_msg
    )
