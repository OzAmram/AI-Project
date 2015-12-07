import random
import copy
from sys import stdin, stdout
from Parser import Parser
from Region import Region
from SuperRegion import SuperRegion


DEBUG = True

class Bot(object):
    def __init__(self):
        self.PICK_STARTING_REGION = 1
        self.PLACE_ARMIES = 2
        self.ATTACK_TRANSFER = 3
        self.armiesLeft = 0
        self.timebank = 0
        self.timePerMove = 0
        self.maxRounds = 0
        self.parser = Parser(self, DEBUG)
        self.phase = None
        self.startingPickAmount = 0
        self.startingRegionsReceived = []
        self.opponentStartingRegions = []
        self.regions = []
        self.superRegions = []
        self.ownedRegions = []
        self.wasteland = []
        self.boarderRegions = set()

    def playGame(self):
        self.parser.parseInput()

    def pickStartingRegion(self):
        if (DEBUG): print "picking starting region"
        #Start here!
        rand_idx = random.randint(0, len(self.startingRegionsReceived)-1) #top bound inclusive
        stdout.write(str(self.startingRegionsReceived[rand_idx]) + "\n")
        stdout.flush()

    def genArmyPlacements(self, armiesToPlace, boarderRegions):
        #generate a list of all possible army placements (a list of lists of move strings), 
        #that only include regions with indexs >= min_region_idx
        # (min_region_idx =0 means include all owned regions)
        if len(boarderRegions) == 0: return [[]]
        #if(min_region_idx == len(boarderRegions)): return [[]] #base case

        #generate all possible placements on regions after this one recursively
        #Then append all possible placements that include a placement onto this region onto those
        region_idx = boarderRegions.pop()
        placements = self.genArmyPlacements(armiesToPlace, boarderRegions)
        for n in xrange(1,armiesToPlace):
            placement = "%s place_armies %d %d" % (self.botName, region_idx, n)
            placements_after = self.genArmyPlacements(armiesToPlace - n, boarderRegions)
            for place_seq in placements_after:
                place_seq.append(placement)
            placements.extend(placements_after)
        #include placement of placing all armies on one territory
        p = "%s place_armies %d %d" % (self.botName, region_idx, armiesToPlace)
        placements.append([p]) 
        return placements


    def placeArmies(self):
        boarderRegions = copy.copy(self.boarderRegions)
        possible_placements = self.genArmyPlacements(self.armiesLeft, boarderRegions)
        #use heuristic to pick best placement immediately
        values = dict()
        for i in xrange(len(possible_placements)):
            val = self.evalPlacementState(possible_placements[i])
            #print values, values.get(val, set())
            values[val] = values.get(val, set()) | set([i])
        max_val = max(values)
        best_placement = possible_placements[values[max_val].pop()]
        self.parser.parseOurMoves(best_placement)
        stdout.write(self.formatMove(best_placement) + "\n")
        stdout.flush()

    def evalRegionImportance(self, region):
        #evaluate if it is important to have armies on this region
        val = 0
        neutralBonus = 4
        opponentBonus = 2
        for i in xrange(region.getNbNeighbors()):
            neighbor_idx = region.getNeighbor(i)
            neighbor = self.regions[neighbor_idx]
            if neighbor.owner == "Neutral":
                val += neutralBonus
            elif neighbor.owner != region.owner:
                val += opponentBonus*neighbor.armies
        return val

    def evalPlacementState(self, placements):
        val = 0
        for placement in placements:
            pieces = placement.split(" ")
            bot = pieces[0]
            region_idx = int(pieces[2])
            armies = int(pieces[3])
            region = self.regions[region_idx]
            val += self.evalRegionImportance(region) * armies
        return val

    def genMoves(self):
        #generate all the possible moves
        moves_per_region = [] #a list of lists of possible moves each region could make
        #each region can only make 1 move
        for region_idx in self.boarderRegions:
            moves = []
            region = self.regions[region_idx]
            if region.getArmies() <= 1: #cant do anything with those armies
                continue
            for k in xrange(region.getNbNeighbors()):
                target = self.regions[region.getNeighbor(k)]
                if (target.getOwner() != "Me" and 
                    region.getArmies() < target.getArmies()*2): continue
                moves.append("%s attack/transfer %d %s %d" 
                            % (self.botName, region.id, target.id, region.getArmies() - 1))
                            #for now only attack/transfer with all armies
            moves_per_region.append(moves)
        return moves_per_region


    def evalMoveState(self, moveStr):
        val = 0
        owner = ""
        pieces = moveStr.split(" ")
        bot = pieces[0]
        owner = bot
        start_idx = int(pieces[2])
        end_idx = int(pieces[3])
        armies = int(pieces[4])
        start = self.regions[start_idx]
        end = self.regions[end_idx]
        if start.owner == end.owner: #transfer
            return self.evalRegionImportance(end) - self.evalRegionImportance(start)

        #otherwise it's an attack
        defendersDestroyed = armies * .6 #assuming deterministic
        attackersDestroyed = end.armies * .7 #again assuming deterministic
        regionBonus = 5 + 5*self.gotSuperRegion(end, start.owner) if defendersDestroyed >= end.armies else 0 
        val += defendersDestroyed - attackersDestroyed + regionBonus
        return val if owner == self.botName else -val

    def gotSuperRegion(self, attackedRegion, owner):
        superRegion_idx = attackedRegion.superRegion
        superRegion= self.superRegions[superRegion_idx]
        for region_idx in superRegion.regions:
            region = self.regions[region_idx]
            if region.owner != owner and attackedRegion != region:
                return 0 #not taken over
        return superRegion.reward

    def makeMoves(self):
        """
        // START HERE!
    /// Output No moves when you have no time left or do not want to commit any moves.
    // std::cout << "No moves "  << std::endl;
    /// Anatomy of a single move
    //  std::cout << botName << " attack/transfer " << from << " " << to << " "<< armiesMoved;
    /// When outputting multiple moves they must be seperated by a comma
        """
        all_moves = self.genMoves()
        best_move = []
        for region_moves in all_moves:
            if len(region_moves) == 0:
                continue
            elif len(region_moves) == 1:
                best_move.append(region_moves[0])
                continue
            values = dict()
            for i in xrange(len(region_moves)):
                val = self.evalMoveState(region_moves[i])
                values[val] = values.get(val, set()) | set([i])
            max_val = max(values)
            best_move.append(region_moves[values[max_val].pop()]) #pick a random best move if there are multiple
        stdout.write(self.formatMove(best_move) + "\n")
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
        regionsToAdd = noSuperRegion - len(self.superRegions) + 1
        if regionsToAdd < 0: regionsToAdd = 0
        for i in xrange(regionsToAdd):
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
        self.startingRegionsReceived = []

    def addStartingRegion(self, noRegion):
        self.startingRegionsReceived.append(noRegion)

    def addOpponentStartingRegion(self, noRegion):
        self.opponentStartingRegions.append(noRegion)


    def makePlacement(self, region_idx, new_armies):
        region = self.regions[region_idx]
        if (region.owner != "Me"): return #something went wrong
        region.setArmies(region.getArmies() + new_armies)
        if(DEBUG): print region.getArmies()

    def makeAttackTransfer(self, fromRegion_idx, toRegion_idx, armies):
        fromRegion = self.regions[fromRegion_idx]
        toRegion = self.regions[toRegion_idx]
        if(fromRegion.owner == "Me" and toRegion.owner == "Me"):
            #transfer
            fromRegion.setArmies(fromRegion.getArmies() - armies)
            toRegion.setArmies(toRegion.getArmies() + armies)
        elif(fromRegion.owner == "Me" and toRegion.owner != "Me"):
            #attack
            defending_armies = toRegion.getArmies()
            expected_defenders_lost = round(0.6*armies)
            expected_attackers_lost = round(0.7*armies)
            if (expected_defenders_lost >= defending_armies):
                #success
                toRegion.setOwner("Me")
                toRegion.setArmies(armies - expected_attackers_lost)
                fromRegion.setArmies(fromRegion.getArmies() - armies)
                self.ownedRegions.append(toRegion_idx)
            else: #failure
                toRegion.setArmies(toRegion.getArmies() - expected_defenders_lost)
                fromRegion.setArmies(fromRegion.getArmies() - expected_attackers_lost)



    def setPhase(self, phase):
        self.phase = phase

    def executeAction(self):
        #print self.ownedRegions
        #print self.boarderRegions
        if self.phase == None:
            return
        if self.phase == self.PICK_STARTING_REGION:
            self.pickStartingRegion()
        elif self.phase == self.PLACE_ARMIES:
            self.placeArmies()
        elif self.phase == self.ATTACK_TRANSFER:
            self.makeMoves()
        self.phase = None

    def updateRegion(self, noRegion, playerName, nbArmies):
        if playerName == self.botName:
            owner = "Me"
        elif playerName == self.opponentBotName:
            owner = "Enemy"
        else:
            owner = "Neutral"
        self.regions[noRegion].setArmies(nbArmies)
        self.regions[noRegion].setOwner(owner)
        if owner == "Me":
            self.ownedRegions.append(noRegion)

    def updateBoarderRegions(self):
        #print "updating boarders"
        for region_idx in self.ownedRegions:
         #   print "checking" + str(region_idx)
            region = self.regions[region_idx]
            for i in xrange(region.getNbNeighbors()):
                neighbor = self.regions[region.getNeighbor(i)]
                if neighbor.owner != "Me":
                    self.boarderRegions.add(region_idx)
                    break
        #print "final boarders" + str(self.boarderRegions)

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
        self.ownedRegions = []
        self.boarderRegions = set()

    def setStartingPickAmount(self, amount):
        self.startingPickAmount = amount

    def formatMove(self, moves):
        #if we don't wont to make a move, return no moves not empty string
        if (len(moves) == 0): return "No moves"

        output = ""
        for move in moves:
            if (output != ""): output += ", "
            output += move

        return output

if __name__ == '__main__':
    Bot().playGame()
