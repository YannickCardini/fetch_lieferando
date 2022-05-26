class Restaurant(object):

    def __init__(self):
        self.names = []
        self.reviews = []
        self.citys = []
        self.owners = []

    def appendData(self,name,owner,city,review):
        self.names.append(name)
        self.reviews.append(review)
        self.citys.append(city)
        self.owners.append(owner)


