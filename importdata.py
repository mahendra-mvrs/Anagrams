import webapp2
import jinja2
import os

from anagram import Anagram
from services import Services


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class ImportData(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"

        message= "Select the file to upload"

        template_values={
            'message': message
        }

        template = JINJA_ENVIRONMENT.get_template("importdata.html")
        self.response.write(template.render(template_values))


    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        file = self.request.get("textfile")
        openFile = open(file)
        readLine = openFile.readline()


        while readLine:

            text_word = (readLine.strip('\n\r')).lower()
            sorted_key = Services().sorted_key(word=text_word)

            list_word = Anagram.query()
            list_word = list_word.filter(Anagram.anagram_key == sorted_key,
                                             Anagram.user_id == Services().get_current_user_id())
            list_word = list_word.fetch()

            valid_permutation = Services().validpermutations(text=sorted_key)

            if len(valid_permutation) > 0:

                if len(list_word) > 0:

                    anagram = list_word[0]

                    if text_word not in anagram.inputed_words:
                        inputed_words = anagram.inputed_words
                        inputed_words.append(text_word)
                        anagram.inputed_words = inputed_words
                        anagram.inputed_words_count = anagram.inputed_words_count + 1
                        anagram.put()

                else:

                    new_anagram = Anagram(anagram_key=sorted_key,
                                          anagram_words=Services().possiblepermutations(text=sorted_key),
                                          inputed_words=[text_word],
                                          inputed_words_count=1,
                                          word_length=len(text_word),
                                          user_id=Services().get_current_user_id())
                    new_anagram.put()

            readLine = openFile.readline()

        openFile.close()

        message = "Upload completed"

        template_values = {
            'message': message
        }

        template = JINJA_ENVIRONMENT.get_template("importdata.html")
        self.response.write(template.render(template_values))
