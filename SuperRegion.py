class SuperRegion(object):

    def __init__(self, reward=0):
        self.reward = reward
        self.regions = []

    def addRegion(self, region):
        self.regions.append(region)
