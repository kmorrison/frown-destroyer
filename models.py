from google.appengine.ext import ndb

class Post(ndb.Model):
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    link = ndb.StringProperty()
    comments = ndb.TextProperty()
    is_seen = ndb.BooleanProperty()
