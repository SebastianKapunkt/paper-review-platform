from app import app, db
from app.models import Role


class Role_Controller():
    """ Class to handle role based Requests """

    def get_roles(self):
        roles = Role.query.all()
        return roles
