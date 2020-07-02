from google.appengine.ext import ndb

# model for the anagram
class Anagram(ndb.Model):
    anagram_key = ndb.StringProperty()
    anagram_words = ndb.StringProperty(repeated = True)
    input_words = ndb.StringProperty(repeated = True)
    input_words_count = ndb.IntegerProperty()
    word_length = ndb.IntegerProperty()
    user_id = ndb.StringProperty()



