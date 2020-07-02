import webapp2
import jinja2
import os


from anagram import Anagram
from service import Services

# environment creation
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class Info(webapp2.RequestHandler):
# getting data from the db
    def get(self):
# getting the data from the inputed word and storing in the anagram model which has all the words
        self.response.headers["Content-Type"] = "text/html"
        input_word = self.request.GET.get("input_word")
        sorted_key = Services().sorted_key(word=input_word)
        anagram_query = Anagram.query(Anagram.user_id == Services().get_current_user_id())
        possible_combination_key = Services().AllPermutations(text=sorted_key)
        anagram_models = []
# filtering the words which has same key values
        for word in possible_combination_key:
            query = anagram_query.filter(Anagram.anagram_key == word).fetch(projection=[Anagram.input_words])
# checking whether the query has more than one word
            if len(query) > 0:

                for anagram in query:
                    anagram_models.extend(anagram.input_words)
        dictionary_words = {}
# doing appending operation adn storing in dict word
        for word in anagram_models:
            if len(word) in dictionary_words:
                dict_words = dictionary_words[len(word)]
                dict_words.append(word)
                dictionary_words[len(word)] = dict_words
            else:
                dictionary_words[len(word)] = [word]
# template value store the required feilds of data to access
        template_values = {
            "inputword":input_word,
            "dictionary_words": dictionary_words
        }

# environment for connect to the info.html page
        template = JINJA_ENVIRONMENT.get_template("info.html")
        self.response.write(template.render(template_values))
# posting data to the database
    def post(self):
# checking if teh request is cancel or not
        self.response.headers["Content-Type"] = "text/html"
        if self.request.get("cancel"):
            self.redirect("/")


