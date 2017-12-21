from app import app, db
from app.models import User
from passlib.hash import sha256_crypt


class User_Controller:
    """ Class to Handle user Specifiy Queries"""

    def create_user(self, username, email, password, first_name, last_name):
        """ Create a new user if a user with the entered email does not exist """
        new_user = User(
            username=username,
            email=email,
            password=sha256_crypt.encrypt(password),
            reset_password_token='',
            first_name=first_name,
            last_name=last_name,
            role_name='default'
        )

        user_with_email = User.query.filter_by(email=email).first()
        user_with_name = User.query.filter_by(username=username).first()
        if user_with_email or user_with_name:
            return 'exists'
        else:
            db.session.add(new_user)
            db.session.commit()
            return 'ok'

    def authenticate_user(self, email, password):
        """ Authenticate the User by Email and Password """
        user = User.query.filter_by(email=email).first()
        if user:
            if sha256_crypt.verify(str(password), user.password):
                return {
                    'user_id': user.id,
                    'username': user.username,
                    'role': user.role_name,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
        else:
            return None

    def set_user_role(self, user_ids, role):
        """ Set the role of the current User / Admin Only """
        for user_id in user_ids:
            user = User.query.get(user_id)
            user.role_name = role
            db.session.commit()

    def get_current_user_role(self, user_id):
        """ Get the role of the current User which is Logged in """
        user = User.query.get(user_id)
        return user.role_name

    def get_users(self):
        users_dict = []
        users = User.query.all()

        for user in users:
            if user.role_name != 'admin':
                users_dict.append({
                    'user_id': user.id,
                    'username': user.username,
                    'role': user.role_name
                })

        return users_dict

    def list(self):
        user_without_admin = []
        users = User.query.all()

        for user in users:
            if user.role_name != 'admin':
                user_without_admin.append(user)

        return user_without_admin
