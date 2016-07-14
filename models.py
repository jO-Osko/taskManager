# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Task (ndb.Model):
    dodan = ndb.TimeProperty(auto_now_add=True)
    naslov = ndb.StringProperty()
    besedilo = ndb.TextProperty()
    dokoncano = ndb.IntegerProperty(default=0)
    aktiven = ndb.BooleanProperty(default=True)
    pomembnost = ndb.IntegerProperty()

