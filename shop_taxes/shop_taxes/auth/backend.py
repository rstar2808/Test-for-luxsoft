import django_couch
from django.conf import settings
from django_couch.auth.utils import check_password
from couchdbcurl.client import ResourceNotFound
from shop_taxes.models import CustomUser


class CouchBackend(object):

    def __init__(self):
        self.db = django_couch.db(settings.COUCHDB_AUTH_DB)

    def get_user(self, user_id):
        try:
            user = CustomUser.load(user_id)
            if len(self.db.view(settings.COUCHDB_AUTH_VIEW, key=user.username, limit=1).rows):
                return user
            else:
                return None
        except ResourceNotFound:
            return None

    def authenticate(self, username, password):
        db = django_couch.db('db')
        rows = self.db.view(settings.COUCHDB_AUTH_VIEW, key=username.lower(), include_docs=True, limit=1).rows

        if len(rows) and check_password(password, rows[0].value):
            return CustomUser(db[rows[0].id])
        pass
