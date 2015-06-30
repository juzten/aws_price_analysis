# -*- coding: utf-8 -*-

from flask import Flask
from config import config
from APA.views import general

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY
app.debug = config.DEBUG

# custom jinja line delimeters
app.jinja_env.line_statement_prefix = '%'
app.jinja_env.line_comment_prefix = '##'

# register views
app.register_blueprint(general.mod)