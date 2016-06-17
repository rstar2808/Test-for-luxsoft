# -*- coding: utf-8 -*-
import django_couch

from datetime import datetime

from django.conf import settings
from django_couch.auth.backend import User
from couchdbcurl import ResourceNotFound
from django.shortcuts import Http404


class CustomUser(User):
    """Custom user for recursive perms check in templates"""

    def __init__(self, *args, **kwargs):
        self._db = django_couch.db('db')
        self.type = 'user'
        now = datetime.now()
        self.is_active = True
        self.is_superuser = True
        self.joined = now.strftime(settings.DATETIME_FMT)

        super(User, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return u"User %s" % self.get('username')

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

    @staticmethod
    def load(user_id):
        db = django_couch.db('db')
        try:
            doc = CustomUser(db[user_id])
        except ResourceNotFound:
            raise Http404(u"User '%s' not found" % user_id)
        assert doc.type == 'user', "Invalid data loaded"
        return doc