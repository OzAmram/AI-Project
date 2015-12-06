import random
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
        self.regions = []
        self.superRegions = []
        self.ownedRegions = []
        self.wasteland = []

    def playGame(self):
        self.parser.parseInput()

    def pickStartingRegion(self):
        print "picking starting region"
        #Start here!
        rand_idx = random.randint(0, len(self.startingRegionsReceived)-1) #top bound inclusive
        stdout.write(str(self.startingRegionsReceived[rand_idx]) + "\n")
        stdout.flush()

    def genArmyPlacements(self, armiesToPlace, min_region_idx):
        #generate a list of all possible army placements (a list of lists of move strings), 
        #that only include regions with indexs >= min_region_idx
        # (min_region_idx =0 means include all owned regions)
        
        if(min_region_idx == len(self.ownedRegions)): return [[]] #base case

        #generate all possible placements on regions after this one recursively
        #Then append all possible placements that include a placement onto this region onto those
        placements = self.genArmyPlacements(armiesToPlace, min_region_idx + 1)
        region_idx = self.ownedRegions[min_region_idx]
        for n in range(1,armiesToPlace):
            placement = "%s place_armies %d %d" % (self.botName, region_idx, n)
            placements_after = self.genArmyPlacements(armiesToPlace - n, min_region_idx +1)
            for place_seq in placements_after:
                place_seq.append(placement)
            placements.extend(placements_after)
        #include placement of placing all armies on one territory
        p = "%s place_armies %d %d" % (self.botName, region_idx, armiesToPlace)
        placements.append([p]) 
        return placements


    def placeArmies(self):
        #start here!
        possible_placements = self.genArmyPlacements(self.armiesLeft, 0)
        #use heuristic to pick best placement immediately
        values = [self.evalPlacementState(possible_placements[i]) for i in xrange(len(possible_placements))]
        max_val = max(values)
        best_placement = possible_placements[values.index(max_val)]
        stdout.write(self.formatMove(best_placement) + "\n")
        stdout.flush()

    def evalPlacementState(self, placements):
        val = 0
        neutralBonus = 50
        opponentBonus = 25
        for placement in placements:
            pieces = placement.split(" ")
            bot = pieces[0]
            region_idx = int(pieces[2])
            armies = int(pieces[3])
            region = self.regions[region_idx]
            for i in xrange(region.getNbNeighbors()):
                neighbor_idx = region.getNeighbor(i)
                neighbor = self.regions[neighbor_idx]
                if neighbor.owner == "Neutral":
                    val += neutralBonus
                elif neighbor.owner != region.owner:
                    val += opponentBonus
        return val

    def genMoves(self):
        #generate all the possible moves
        moves_per_region = [] #a list of lists of possible moves each region could make
        #each region can only make 1 move
        for j in xrange(len(self.ownedRegions)):
            region = self.regions[self.ownedRegions[j]]
            moves = []
            if region.getArmies() <= 1: #cant do anything with those armies
                continue
            for k in range(region.getNbNeighbors()):
                target = self.regions[region.getNeighbor(k)]
                if (target.getOwner() != "Me" and 
                    region.getArmies() <= target.getArmies()): pass
                moves.append("%s attack/transfer %d %s %d," 
                            % (self.botName, region.id, target.id, region.getArmies() - 1))
                            #for now only attack/transfer with all armies
            moves_per_region.append(moves)


        #generate all the possible permuations of moves
        #each permuataion can only have 1 move for each region
        perm_moves = [[]]
        for region_moves in moves_per_region:
            additional_perms = []
            for move in region_moves:
                for move_list in perm_moves:
                    additional_perms.append(move_list.append(move))
            perm_moves.extend(additional_perms)

        return perm_moves

    def evalMoveState(self, moveStr):
        val = 0
        for move in moveStr:
            #convert from move string to a state to be evaluated
            pieces = move.split(" ")
            bot = pieces[0]
            start_idx = int(pieces[2])
            end_idx = int(pieces[3])
            armies = int(pieces[4])
            start = self.regions[start_idx]
            end = self.regions[end_idx]
            if start.owner == end.owner: return 0 #transfer, no effect?
            #otherwise it's an attack
            defendersDestroyed = amries * .6 #assuming deterministic
            attackersDestroyed = end.armies * .7 #again assuming deterministic
            regionBonus = 10 + 100*self.gotSuperRegion(end, start.owner) if defendersDestroyed >= end.armies else 0 
            val += defendersDestroyed - attackersDestroyed + regionBonus
        return val if bot == self.botName else -val

    def gotSuperRegion(self, attackedRegion, owner):
        superRegion = attackedRegion.superRegion
        for region in superRegion.regions:
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
        values = [self.evalMoveState(all_moves[i]) for i in xrange(len(all_moves))]
        max_val = max(values)
        best_move = all_moves[values.index(max_val)]
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
        for i in range(regionsToAdd):
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
