from sys import stdin, stdout
import copy

class Parser(object):
    def __init__(self, bot, DEBUG=False):
        self.DEBUG = DEBUG
        self.bot = bot

    def parseInput(self):
        inputType = stdin.readline().strip().split(" ")
        while(len(inputType) != 0):
            if(self.DEBUG): print inputType
            if inputType[0] == "setup_map":
                self.parseSetupMap(inputType[1:])
            elif inputType[0] == "settings":
                self.parseSettings(inputType[1:])
            elif inputType[0] == "update_map":
                self.parseUpdateMap(inputType[1:])
            elif inputType[0] == "pick_starting_region":
                self.parsePickStartingRegion(inputType[1:])
            elif inputType[0] == "go":
                self.parseGo(inputType[1:])
            else:
                #getline(std::cin, line)
                #std::cerr << inputType << " " << line << std::endl
                pass

            self.bot.executeAction()
            inputType = stdin.readline().strip().split(" ")

    def parseSetupMap(self, inputStr):
        setupType = inputStr[0]
        if setupType == "super_regions":
            self.parseSuperRegions(inputStr[1:])
        elif setupType == "regions":
            self.parseRegions(inputStr[1:])
        elif setupType == "neighbors":
            self.parseNeighbors(inputStr[1:])
        elif setupType == "wastelands":
            self.parseWastelands(inputStr[1:])
        elif setupType == "opponent_starting_regions":
            self.parseOpponentStartingRegions(inputStr[1:])

    def parseSettings(self, inputStr):
        settingType = inputStr[0]
        if settingType == "timebank":
            timebank = int(inputStr[1])
            self.bot.setTimebank(timebank)
        elif settingType == "time_per_move":
            timePerMove = int(inputStr[1])
            self.bot.setTimePerMove(timePerMove)
        elif settingType == "max_rounds":
            maxRounds = int(inputStr[1])
            self.bot.setMaxRounds(maxRounds)
        elif settingType == "your_bot":
            bot_name = inputStr[1]
            self.bot.setBotName(bot_name)
        elif settingType == "opponent_bot":
            bot_name = inputStr[1]
            self.bot.setOpponentBotName(bot_name)
        elif settingType == "starting_armies":
            armies = int(inputStr[1])
            self.bot.setArmiesLeft(armies)
        elif settingType == "starting_regions":
            noRegions = inputStr[1:]
            for noRegion in noRegions:
                self.bot.addStartingRegion(noRegion)
        elif settingType == "starting_pick_amount":
            #added by Oz
            amount = int(inputStr[1])
            self.parseStartingPickAmount(amount)

    def parseUpdateMap(self, inputStr):
        self.bot.resetRegionsOwned()
        for i in xrange(0, len(inputStr), 3):
            noRegion = int(inputStr[i])
            playerName = inputStr[i+1]
            armies = int(inputStr[i+2])
            self.bot.updateRegion(noRegion, playerName, armies)
        self.bot.updateBoarderRegions()

    def parseMoves(self, Regions, Moves):
        regions = copy.deepcopy(Regions)
        for move in Moves:
            if (move == "No moves"): continue
            pieces = move.split(" ")
            if (pieces[1] == "place_armies"):
                if(self.DEBUG): print "parsing our placements"
                #Place armies move
                region_idx = int(pieces[2])
                armies = int(pieces[3])
                self.bot.makePlacement(regions, region_idx, armies)
            elif (pieces[1] == "attack/transfer"):
                    fromRegion_idx = int(pieces[2])
                    toRegion_idx = int(pieces[3])
                    armies = int(pieces[4])
                    self.bot.makeAttackTransfer(regions, fromRegion_idx, toRegion_idx, armies)
        return regions

    def parseGo(self, inputStr):
        words = inputStr
        phase = words[0]
        delay = int(words[1])
        if phase == "place_armies":
            self.bot.setPhase(self.bot.PLACE_ARMIES)
            return
        if phase == "attack/transfer":
            self.bot.setPhase(self.bot.ATTACK_TRANSFER)
            return
        assert(False) #supposed to raise an error

    def parseSuperRegions(self, inputStr):
        words = inputStr
        for i in range(0, len(words), 2):
            superReg = int(words[i])
            reward = int(words[i+1])
            self.bot.addSuperRegion(superReg, reward)

    def parseRegions(self, inputStr):
        words = inputStr
        for i in range(0, len(words), 2):
            reg = int(words[i])
            reward = int(words[i+1])
            self.bot.addRegion(reg, reward)

    def parsePickStartingRegion(self, inputStr):
        delay = int(inputStr[0])
        self.bot.clearStartingRegions()
        regions = inputStr[1:]
        for region in regions:
            self.bot.addStartingRegion(int(region))
        self.bot.setPhase(self.bot.PICK_STARTING_REGION)

    def parseOpponentStartingRegions(self, inputStr):
        noRegions = inputStr
        for noRegion in noRegions:
            self.bot.addOpponentStartingRegion(int(noRegion))

    def parseNeighbors(self, inputStr):
        words = inputStr
        for i in range(0, len(words), 2):
            region = int(words[i])
            neighbors = words[i+1]
            neighbors_flds = neighbors.split(",")
            for i in neighbors_flds:
                self.bot.addNeighbors(region, int(i))

        #TODO:
        #self.bot.setPhase(self.bot.FIND_BORDERS)

    def parseWastelands(self, inputStr):
        regions = inputStr
        for region in regions:
            self.bot.addWasteland(int(region))

    def parseStartingPickAmount(self, amount):
        self.bot.startingPickAmount = amount
