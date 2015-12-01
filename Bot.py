import random
from sys import stdin, stdout
from Parser import Parser
from Region import Region
from SuperRegion import SuperRegion

class Bot(object):
    PICK_STARTING_REGION = 1
    PLACE_ARMIES = 2
    ATTACK_TRANSFER = 3
    def __init__(self):
        self.armiesLeft = 0
        self.timebank = 0
        self.timePerMove = 0
        self.maxRounds = 0
        self.parser = Parser(self)
        self.phase = None

    def playGame(self):
        self.parser.parseInput()

    def pickStartingRegion(self):
        #Start here!
        stdout.write(self.startingRegionsreceived)
        stdout.flush()

    def placeArmies(self):
        #start here!
        self.region = random.randint(len(ownedRegions))
        move = "%s place_armies %d %d" % (self.botName, self.ownedRegions[region], self.armiesLeft)
        stdout.write(move)
        stdout.flush()
        self.addArmies(self.ownedRegions[region], self.armiesLeft)

    def makeMoves(self):
        """
        // START HERE!
    /// Output No moves when you have no time left or do not want to commit any moves.
    // std::cout << "No moves "  << std::endl;
    /// Anatomy of a single move
    //  std::cout << botName << " attack/transfer " << from << " " << to << " "<< armiesMoved;
    /// When outputting multiple moves they must be seperated by a comma
        """
        move = ""
        for j in range(len(self.ownedRegions)):
            i = self.ownedRegions[j]
            if self.regions[i].getArmies() <= 1:
                continue
            target = self.regions[i].getNeighbor(self.regions[i].getNbNeighbors())
            for k in range(5):
                if self.regions[target].getOwner() != "Me":
                    break
                target = self.regions[i].getNeighbor(self.regions[i].getNbNeighbors())
            move += "%s attack/transfer %d %s %d," % (self.botName, i, 
                target, self.regions[i].getArmies() - 1)
        if move != "": move = move[:-1] #strip last comma
        stdout.write(move)
        stdout.flush()

    def addRegion(self, noRegion, noSuperRegion):
        while(len(self.regions) <= noRegion):
            self.regions.append(Region())
        self.regions[noRegion] = Region(noRegion, noSuperRegion)
        self.superRegions[noSuperRegion].addRegion(noRegion)

    def addNeighbors(self, noRegion, neighbors):
        self.regions[noRegion].addNeighbor(neighbors)
        self.regions[neighbors].addNeighbor(noRegion)

    def addWasteland(self, noRegion):
        self.wasteland.append(noRegion)

    def addSuperRegion(self, noSuperRegion, reward):
        while(len(self.superRegions) <= noSuperRegion):
            self.superRegions.append(SuperRegion())
        self.superRegions[noSuperRegion] = SuperRegion(reward)

    def setBotName(self, name):
        self.botName = name

    def setOpponentBotName(self, name):
        self.opponentBotName = name

    def setArmiesLeft(self, nbArmies):
        self.armiesLeft = nbArmies

    def setTimebank(self, newTimebank):
        self.timebank = newTimebank

    def setTimePerMove(self, newTimePerMove):
        self.timePerMove = newTimePerMove

    def setMaxRounds(self, newMaxRounds):
        self.maxRounds = newMaxRounds

    def clearStartingRegions(self):
        self.startingRegionsreceived.clear()

    def addStartingRegion(self, noRegion):
        self.startingRegionsreceived.append(noRegion)

    def addOpponentStartingRegion(self, noRegion):
        self.opponentStartingRegions.append(noRegion)

    def opponentPlacement(self, noRegion, nbArmies):
        #TODO: STUB
        pass

    def opponentMovement(self, noRegion, toRegion, nbArmies):
        #TODO: STUB
        pass

    def startDelay(self, delay):
        #TODO: STUB
        pass

    def setPhase(self, phase):
        self.phase = phase

    def executeAction(self):
        if self.phase == None:
            return
        if self.phase == PICK_STARTING_REGION:
            self.pickStartingRegion()
        elif phase == PLACE_ARMIES:
            self.place_armies()
        elif phase == ATTACK_TRANSFER:
            self.makeMoves()
        phase = None

    def updateRegion(self, noRegion, playerName, nbArmies):
        if playerName == self.botName:
            self.owner = "Me"
        elif playerName == self.opponentBotName:
            self.owner = "Enemy"
        else:
            self.owner = "Neutral"
        self.regions[noRegion].setArmies(nbArmies)
        self.regions[noRegion].setOwner(owner)
        if owner == "Me":
            self.ownedRegions.append(noRegion)

    def addArmies(self, noRegion, nbArmies):
        self.regions[noRegion].setArmies(self.regions[noRegion].getArmies() + nbArmies)

    def moveArmies(self, noRegion, toRegion, nbArmies):
        if (self.regions[noRegion].getOwner() == self.regions[toRegion].getOwner() and
            self.regions[noRegion].getArmies() > nbArmies):
            self.regions[noRegion].setArmies(self.regions[noRegion].getArmies() -
                                                nbArmies)
            self.regions[toRegion].setArmies(self.regions[toRegion].getArmies() +
                                                nbArmies)
        elif self.regions[noRegion].getArmies() > nbArmies:
            self.regions[noRegion].setArmies(self.regions[noRegion].getArmies - 
                                                nbArmies)
            if self.regions[toRegion].getArmies() - round(nbArmies * 0.6) <= 0:
                self.regions[toRegion].setArmies(nbArmies - 
                        round(self.regions[toRegion].getArmies() * 0.7))
                self.regions[toRegion].setOwner(self.regions[noRegion].getOwner())
            else:
                self.regions[noRegion].setArmies(self.regions[noRegion].getArmies() +
                    nbArmies - round(self.regions[toRegion].getArmies() * 0.7))
                self.regions[toRegion].setArmies(self.regions[toRegion].getArmies() - 
                    round(nbArmies * 0.6))

    def resetRegionsOwned(self):
        self.ownedRegions.clear()


if __name__ == '__main__':
    Bot().playGame()
