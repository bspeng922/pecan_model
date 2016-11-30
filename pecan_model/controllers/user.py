import hashlib
import logging

import pecan
from pecan import expose


LOG = logging.getLogger()


class UserController(object):
    def _encrypted_password(self, password):
        return hashlib.md5(password).hexdigest()

    @expose('json')
    def index(self):
        return {'msg': 'user index'}

    @expose('json')
    @expose(generic=True)
    def register(self):
        return {'message': 'Please use post method'}

    @expose('json')
    @expose(generic=True)
    def login(self):
        return {'message': 'Please use post method'}

    @expose('json')
    @expose(generic=True)
    def change_pwd(self):
        return {'message': 'Please use post method'}

    @register.when(method='POST', template='json')
    def register_POST(self):
        username = pecan.request.POST.get('username')
        password = pecan.request.POST.get('password')
        email = pecan.request.POST.get('email')
        if not username or not password:
            return {"message": "Unable to register user, params not legal.",
                    "code": "400"}

        db_conn = pecan.request.db_conn
        # if get user by username then return 401
        if db_conn.get_user(username=username):
            return {"message": "Unable to register user, user already exists.",
                    "code": "401"}

        # create user
        try:
            db_conn.create_user(username, self._encrypted_password(password), email)
            return {"message": "Successfully registed a new user.",
                    "code": "200"}
        except Exception, e:
            pass

        return {"message": "Unable to register user, unknown error.",
                "code": "401"}

    @login.when(method='POST', template='json')
    def login_POST(self):
        username = pecan.request.POST.get('username')
        password = pecan.request.POST.get('password')

        db_conn = pecan.request.db_conn
        user = db_conn.get_user(username)
        if not user:
            return {"message": "Unable to login , username not found.",
                    "code": "401"}

        if user.password == self._encrypted_password(password):
            return {"message": "Successfully login.",
                    "code": "200"}
        return {"message": "Unable to login , wrong password.",
                "code": "401"}

    @change_pwd.when(method='POST', template='json')
    def change_pwd_POST(self):
        username = pecan.request.POST.get('username')
        password = pecan.request.POST.get('password')
        new_password = pecan.request.POST.get('new_password')

        db_conn = pecan.request.db_conn
        user = db_conn.get_user(username)

        if user.password != self._encrypted_password(password):
            return {"message": "Unable to update password for user %s , "
                               "wrong password." % username.encode("utf-8"),
                    "code": "401"}

        try:
            # update user's password
            db_conn.update_user(username, self._encrypted_password(new_password))
            return {"message": "Successfully updated user %s." % username.encode("utf-8"),
                    "code": "200"}
        except Exception, e:
            pass

        return {"message": "Unable to update password for user %s , "
                           "unknown error." % username.encode("utf-8"),
                "code": "401"}
