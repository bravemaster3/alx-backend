#!/usr/bin/env python3
"""
basic Flask app
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from pytz import UnknownTimeZoneError

app = Flask(__name__)
babel = Babel(app)


class Config:
    """babel config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """gets locale from request"""
    if 'locale' in request.args:
        locale = request.args['locale']
        if locale in app.config['LANGUAGES']:
            return locale

    # Check if user settings exist and the locale is supported
    if g.user and 'locale' in g.user:
        user_locale = g.user['locale']
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    request_locale = request.accept_languages.best_match(
        app.config['LANGUAGES'])

    # If no supported locale is found in the request header,
    # fall back to the default locale
    return request_locale or app.config['BABEL_DEFAULT_LOCALE']


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Get user information from mock user table."""
    return users.get(user_id)


@app.before_request
def before_request():
    """Before request hook to set the user globally."""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.timezoneselector
def get_timezone():
    # Check if the 'timezone' parameter is present in the URL parameters
    if 'timezone' in request.args:
        timezone = request.args['timezone']
        # Check if the provided timezone is valid
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    # Check if user settings exist and the timezone is valid
    if g.user and 'timezone' in g.user:
        user_timezone = g.user['timezone']
        try:
            pytz.timezone(user_timezone)
            return user_timezone
        except UnknownTimeZoneError:
            pass

    # Default to UTC if no valid timezone is found
    return 'UTC'

@app.route('/')
def index():
    """renders a simple page"""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(debug=True)
