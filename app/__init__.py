"""Main Flask app
"""
import os
from flask import Flask
from app import routes


app = Flask(__name__)
app.config.update({'SECRET_KEY': os.environ.get('SECRET_KEY')})
# alternatively SECRET_KEY = os.urandom(32)
app.register_blueprint(routes.bp)
