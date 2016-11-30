from base import get_session

from sqlalchemy.orm import exc

from pecan_model.model import user as user_model


class Connection(object):
    def __init__(self):
        pass

    def get_user(self, username):
        query = get_session().query(user_model.User).filter_by(name=username)
        try:
            return query.one()
        except exc.NoResultFound:
            pass

        return None

    def list_users(self):
        session = get_session()
        query = session.query(user_model.User)
        users = query.all()
        return users

    def create_user(self, username, password, email=None):
        session = get_session()
        user = user_model.User()
        user.name = username
        user.password = password
        if email:
            user.email = email
        session.add(user)
        session.commit()

    def update_user(self, username, password, email=None):
        update_dict = {'password': password}
        if email:
            update_dict['email'] = email
        session = get_session()
        query = session.query(user_model.User).filter_by(name=username)
        query.update(update_dict)
        session.commit()

    def delete_user(self, username):
        session = get_session()
        session.query(user_model.User).filter_by(name=username).delete()
        session.commit()
