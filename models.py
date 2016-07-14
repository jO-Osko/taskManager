# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Task (ndb.Model):
    dodan = ndb.TimeProperty(auto_now_add=True)
    naslov = ndb.StringProperty()
    besedilo = ndb.TextProperty()
    dokoncano = ndb.FloatProperty(default=0.0)
    aktiven = ndb.BooleanProperty(default=True)
    pomembnost = ndb.IntegerProperty()

