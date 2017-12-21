from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

from app import models
db.init_app(app)

from app import db_init
with app.app_context():
    db.create_all()
    db_init.init_db()


from app import user_controller, paper_controller, role_controller
user_controller = user_controller.User_Controller()
paper_controller = paper_controller.Paper_Controller()
role_controller = role_controller.Role_Controller()

from app import url_for
from app import views
