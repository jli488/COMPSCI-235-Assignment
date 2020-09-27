from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class MovieSearchForm(FlaskForm):
    search_by = SelectField(label='Search By', choices=['Actor', 'Director', 'Genre'])
    search_text = StringField(label='Search Text')
    submit = SubmitField(label='Search')
