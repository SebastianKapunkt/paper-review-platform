from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

from app import models
db.init_app(app)
with app.app_context():
    db.create_all()


from app import user_controller
user_controller = user_controller.User_Controller()

from app import views
