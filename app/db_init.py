from flask import session
from app.models import Role, User
from app import db
from app.user_controller import User_Controller
from passlib.hash import sha256_crypt

def init_db():
    if not User.query.filter_by(username='admin').first():
        user_controller = User_Controller()
        council = Role()
        reviewer = Role()
        council.name = 'council'
        reviewer.name = 'default'
        db.session.add(council)
        db.session.add(reviewer)
        
        #default admin account
        user_controller.create_user('admin', 'admin@paper-review.org', 'superpassword', ' ', ' ')
        admin = User.query.filter_by(username='admin').first()
        user_controller.set_user_role({admin.id}, 'admin')

        #default council (Conference Chair)
        user_controller.create_user(username='council', first_name='Conference', last_name='Chair', email='council@paper-review.org', password='council')

        #default user
        user_controller.create_user(username='clara', first_name='Clara', last_name='Sanders', email='clara@paper-review.org', password='clara')
        user_controller.create_user(username='peter', first_name='Peter', last_name='Eggerts', email='peter@paper-review.org', password='peter')
        user_controller.create_user(username='julia', first_name='Julia', last_name='Swanson', email='julia@paper-review.org', password='julia')
        user_controller.create_user(username='maria', first_name='Maria', last_name='Steffan', email='maria@paper-review.org', password='maria')
        user_controller.create_user(username='elias', first_name='Elias', last_name='Lorenzo', email='elias@paper-review.org', password='elias')
        
        db.session.commit()

