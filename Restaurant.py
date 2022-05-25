from unicodedata import name


class Restaurant(object):

    def __init__(self,name='',review='',address='',owner=''):
        self.name = name
        self.review = review
        self.address = address
        self.owner = owner
