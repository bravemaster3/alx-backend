#!/usr/bin/env python3
"""
basic Flask app
"""

from flask import Flask, render_template, request
from flask_babel import Babel

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
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """renders a simple page"""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
