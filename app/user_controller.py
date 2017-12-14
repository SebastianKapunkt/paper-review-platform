from app import app, db
from app.models import User
from passlib.hash import sha256_crypt


class User_Controller:

    def create_user(self, username, email, password, first_name, last_name):
        new_user = User(
            username=username,
            email=email,
            password=sha256_crypt.encrypt(password),
            reset_password_token='',
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(new_user)
        db.session.commit()

    def authenticate_user(self, email, password):
        """ Get the User by Email """
        user = User.query.filter_by(email=email).first()
        print('user: ', user.username)
        if sha256_crypt.verify(str(password), user.password):
            return user.username
        else:
            return None

    def get_users(self):
        users_dict = []
        users = User.query.all()
        print(len(users))

        for user in users:
            users_dict.append({'id':user.id, 'username': user.username})
            print(users_dict)

        return users_dict

    def list(self):
        return User.query.all()
        