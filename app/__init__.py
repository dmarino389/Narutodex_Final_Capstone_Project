from flask import Flask

from flask import Flask
app = Flask(__name__)

from config import Config
app.config.from_object(Config)

from . import routes