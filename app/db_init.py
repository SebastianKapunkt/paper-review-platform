from flask import session
from app.models import Role, User
from app import db
from app.user_controller import User_Controller

def init_db():
    if not User.query.filter_by(username='admin').first():
        user_controller = User_Controller()
        council = Role()
        reviewer = Role()
        council.name = 'council'
        reviewer.name = 'default'
        db.session.add(council)
        db.session.add(reviewer)
        db.session.commit()
        
        user_controller.create_user('admin', 'admin@paper-review.de', 'superpassword', ' ', ' ')
        admin = User.query.filter_by(username='admin').first()
        user_controller.set_user_role({admin.id}, 'admin')