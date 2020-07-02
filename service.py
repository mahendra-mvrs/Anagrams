from google.appengine.ext import ndb
from google.appengine.api import users
from itertools import permutations

from user import MyUser
from anagram import Anagram

class Services(object):

# opening the  valid word file
    with open("validwords.txt") as word_file:
        valid_words = set(word.strip().lower() for word in word_file)


    def get_current_user(self):
        return users.get_current_user()


    def get_current_user_id(self):
        return users.get_current_user().user_id()

# method for getting sorted key
    def sorted_key(self, word):
        chars = [c for c in word]
        chars.sort()
        return "".join(chars)

# method for getting the permutations for the word
    def permutations(self,text):

        return [''.join(p) for p in permutations(text)]

# method for getting all possible permutations for the inputted word
    def AllPermutations(self,text):
        allValues = []
        for i in range(2, len(text) + 1):
            value = [''.join(p) for p in permutations(text, i)]
            allValues.extend(value)
        return allValues

# method for getting all the valid permutations
    def validpermutations(self,text):
        valid_word = []
        possible_combinations = [''.join(p) for p in permutations(text)]
        for p in possible_combinations:
            if p in self.valid_words:
                valid_word.append(p)
        return valid_word
