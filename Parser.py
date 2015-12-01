from sys import stdin, stdout

class Parser(object):
    def __init__(self, bot):
        self.bot = bot

    def parseInput(self):
        inputType = stdin.readline().strip()
        while(inputType != ""):
            if inputType == "setup_map":
                self.parseSetupMap()
            elif inputType == "settings":
                self.parseSettings()
            elif inputType == "update_map":
                self.parseUpdateMap()
            elif inputType == "opponent_moves":
                self.parseOpponentMoves()
            elif inputType == "pick_starting_region":
                self.parsePickStartingRegion()
            elif inputType == "go":
                self.parseGo()
            else:
                #getline(std::cin, line)
                #std::cerr << inputType << " " << line << std::endl
                pass

            self.bot.executeAction()
            inputType = stdin.readline().strip()

    def parseSetupMap(self):
        setupType = stdin.readline().strip()
        if setupType == "super_regions":
            self.parseSuperRegions()
        elif setupType == "regions":
            self.parseRegions()
        elif setupType == "neighbors":
            self.parseNeighbors()
        elif setupType == "wastelands":
            self.parseWastelands()
        elif setupType == "opponent_starting_regions":
            self.parseOpponentStartingRegions()

    def parseSettings(self):
        settingType = stdin.readline().strip()
        if settingType == "timebank":
            timebank = stdin.readline().strip()
            self.bot.setTimebank(timebank)
        elif settingType == "time_per_move":
            timePerMove = stdin.readline().strip()
            self.bot.setTimePerMove(timePerMove)
        elif settingType == "max_rounds":
            maxRounds = stdin.readline().strip()
            self.bot.setMaxRounds(maxRounds)
        elif settingType == "your_bot":
            bot_name = stdin.readline().strip()
            self.bot.setBotName(bot_name)
        elif settingType == "opponent_bot":
            bot_name = stdin.readline().strip()
            self.bot.setOpponentBotName(bot_name)
        elif settingType == "starting_armies":
            armies = stdin.readline().strip()
            self.bot.setArmiesLeft(armies)
        elif settingType == "starting_regions":
            noRegion = stdin.readline().strip()
            while(noRegion != ""):
                self.bot.addStartingRegion(noRegion)
                noRegion = stdin.readline().strip()

    def parseUpdateMap(self):
        self.bot.resetRegionsOwned()
        words = stdin.readline().strip().split(" ")
        while len(words) != 0:
            noRegion = words[0]
            playerName = words[1]
            armies = words[2]
            self.bot.updateRegion(noRegion, playerName, armies)
            words = stdin.readline().strip().split(" ")


    def parseOpponentMoves(self):
        words = stdin.readline().strip().split(" ")
        while len(words) != 0:
            playerName = words[0]
            action = words[1]
            if action == "place_armies":
                move = stdin.readline().strip().split(" ")
                noRegion = move[0]
                armies = move[1]
                self.bot.opponentPlacement(noRegion, armies)
            if action == "attack/transfer":
                move = stdin.readline().strip().split(" ")
                noRegion = move[0]
                toRegion = move[1]
                armies = move[2]
                self.bot.opponentMovement(noRegion, toRegion, armies)

    def parseGo(self):
        words = stdin.readline().strip().split(" ")
        phase = words[0]
        delay = words[1]
        self.bot.startDelay(delay)
        if phase == "place_armies":
            self.bot.setPhase(self.bot.PLACE_ARMIES)
            return
        if phase == "attack/transfer":
            self.bot.setPhase(self.bot.ATTACK_TRANSFER)
            return
        assert(False) #supposed to raise an error

    def parseSuperRegions(self):
        words = stdin.readline().strip().split(" ")
        while len(words) != 0:
            superReg = words[0]
            reward = words[1]
            self.bot.addSuperRegion(superReg, reward)
            words = stdin.readline().strip().split(" ")

    def parseRegions(self):
        words = stdin.readline().strip().split(" ")
        while len(words) != 0:
            reg = words[0]
            reward = words[1]
            self.bot.addRegion(reg, reward)
            words = stdin.readline().strip().split(" ")

    def parsePickStartingRegion(self):
        delay = stdin.readline().strip()
        self.bot.startDelay(delay)
        self.bot.clearStartingRegions()
        region = stdin.readline().strip()
        while(region != ""):
            self.bot.addStartingRegion(region)
            region = stdin.readline().strip()
        self.bot.setPhase(self.bot.PICK_STARTING_REGION)

    def parseOpponentStartingRegions(self):
        noRegion = stdin.readline().strip()
        while (noRegion != ""):
            self.bot.addOpponentStartingRegion(noRegion)
            noRegion = stdin.readline().strip()

    def parseNeighbors(self):
        words = stdin.readline().strip().split(" ")
        while(len(words) != 0):
            region = words[0]
            neighbors = words[1]
            neighbors_flds = neighbors.split(",")
            for i in neighbors_flds:
                self.bot.addNeighbors(region, int(i))
            words = stdin.readline().strip().split(" ")

        #TODO:
        #self.bot.setPhase(self.bot.FIND_BORDERS)

    def parseWastelands(self):
        region = stdin.readline().strip()
        while(region != ""):
            self.bot.addWasteland(region)
            region = stdin.readline().strip()