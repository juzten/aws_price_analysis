# -*- coding: utf-8 -*-

import urllib
import json
import requests
from flask import Blueprint, render_template_string, render_template, flash
from flask import Flask, request, Response, g, session, redirect, url_for
from config import config


mod = Blueprint('general', __name__)


@mod.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@mod.app_errorhandler(500)
def internal_error(error):
    # uncomment if using a database
    # db.session.rollback()
    return render_template('500.html'), 500


@mod.route('/', methods=['POST', 'GET'])
def index():
    """Index."""

    return render_template('index.html')
