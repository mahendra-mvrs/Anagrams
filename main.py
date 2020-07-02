import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

from user import MyUser
from anagram import Anagram
from deviceinfo import Info
from newdevice import NewWord
from service import Services

# environment creation
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class MainHandler(webapp2.RequestHandler):

# gettign data fro the database
    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        user = Services().get_current_user()
        total_count = 0
        unique_anagrams = 0
      #  word_model = Anagram.query()
        anagram_model = None
# checking the user
        if user:
            url = users.create_logout_url(self.request.uri)
            user_key = ndb.Key("MyUser", Services().get_current_user_id())
            user = user_key.get()
# creating user and storing in data base
            if user == None:
                user = MyUser(id=Services().get_current_user_id())
                user.put()
# storing th word in the anagram query and converting them to lower case letters
            anagram_query = Anagram.query(Anagram.user_id == Services().get_current_user_id())
            anagram_count_query = anagram_query.fetch()
            unique_anagrams = len(anagram_count_query)

            for inputed_word in anagram_count_query:
                for word in inputed_word.input_words:
                    total_count += 1
            input_word = self.request.get("input_word").lower()
# checking lenth of the word
            if len(input_word) > 0:
# checking whether the button is search or not
                if self.request.GET.get("search_button") == "Search Word":
# filtering the anagram query
                    anagram_query = anagram_query.filter(Anagram.input_words.IN([input_word]))
# fetching the filterd anagram query
            anagram_model = anagram_query.fetch()
# creating login for user
        else:
            url = users.create_login_url(self.request.uri)
# tempate values storing all the required values
        template_values = {
            "url": url,
            "user": user,
            "anagram_model":anagram_model,
            "unique_anagrams": unique_anagrams,
            "total_count": total_count,
        }
# environment for the templatr values
        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))
# framework connection
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newdevice', NewWord),
    ('/deviceinfo', Info)
], debug=True)

