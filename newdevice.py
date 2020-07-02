import webapp2
import os
import jinja2

from google.appengine.api import users

from anagram import Anagram
from service import Services
# environment creation
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class NewWord(webapp2.RedirectHandler,Services):

# grtting datat from the database
    def get(self):
# getting the data of the newword.html
        self.response.headers["Content-Type"] = "text/html"
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template("newword.html")
        self.response.write(template.render(template_values))
# posting the data to the database
    def post(self):
        self.response.headers["Content-Type"] = "text/html"
# checking whether the key is add word
        if self.request.get("newdevice") == "Add Word":
            inputed_word = self.request.get("word").lower()
# checking whether the inputed word is null or not  and redirecting to the add word paeg
            if Services().get_current_user() == None or inputed_word == None or inputed_word == "" :
                self.redirect("/newdevice")
                return
            current_user_id = Services().get_current_user_id()
            sorted_key = Services().sorted_key(word =inputed_word)
            list_word = Anagram.query()
            list_word = list_word.filter(Anagram.anagram_key == sorted_key,Anagram.user_id == current_user_id)
            list_word = list_word.fetch()
            valid_permutation = Services().validpermutations(text=sorted_key)
# checking whether the inputed word has valid permutations or not
            if len(valid_permutation) == 0:
                self.redirect("/newdevice")
                return
# checking whether the there are any word in the list or redirecting to the add word page
            if len(list_word) > 0:
                anagram = list_word[0]
                if inputed_word in anagram.input_words:
                    self.redirect("/newdevice")
                    return

                inputed_words = anagram.input_words
                inputed_words.append(inputed_word)
                anagram.input_words = inputed_words
                anagram.input_words_count = anagram.input_words_count + 1
                anagram.put()

            else:

                new_anagram = Anagram(anagram_key=sorted_key, anagram_words = Services().permutations(text=sorted_key),
                                      input_words = [inputed_word],
                                    input_words_count = 1,
                                   word_length = len(inputed_word),
                                      user_id = current_user_id)
                new_anagram.put()
        self.redirect("/")









