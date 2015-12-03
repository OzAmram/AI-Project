class Region(object):
    def __init__(self, id=0, superRegion=0, owner="Neutral", armies=0):
        self.id = id
        self.superRegion = superRegion
        self.owner = owner
        self.armies = armies
        self.neighbors = []

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def getNbNeighbors(self):
        return len(self.neighbors)

    def getNeighbor(self, index):
        return self.neighbors[index]

    def getArmies(self):
        return self.armies
