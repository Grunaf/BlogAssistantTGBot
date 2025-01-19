from flask import Flask

app = Flask(__name__)

# Подключение маршрутов
from flask_app.routes import *
