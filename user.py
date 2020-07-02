from google.appengine.ext import ndb
from anagram import Anagram

# model for user
class MyUser(ndb.Model):
    email_address = ndb.StringProperty()


