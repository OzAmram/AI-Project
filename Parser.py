from sys import stdin, stdout

class Parser(object):
    def __init__(self, bot):
        self.bot = bot

    def parseInput(self):
        while(std::cin >> inputType):
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
                getline(std::cin, line)
                std::cerr << inputType << " " << line << std::endl

            self.bot.executeAction()

    def parseSetupMap(self):
        setupType = stdin.readline()
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
        settingType = stdin.readline()
        if settingType == "timebank":
            timebank = stdin.readline()
            self.bot.setTimebank(timebank)
        elif settingType == "time_per_move":
            timePerMove = stdin.readline()
            self.bot.setTimePerMove(timePerMove)
        elif settingType == "max_rounds":
            maxRounds = stdin.readline()
            self.bot.setMaxRounds(maxRounds)
        elif settingType == "your_bot":
            bot_name = stdin.readline()
            self.bot.setBotName(bot_name)
        elif settingType == "opponent_bot":
            bot_name = stdin.readline()
            self.bot.setOpponentBotName(bot_name)
        elif settingType == "starting_armies":
            armies = stdin.readline()
            self.bot.setArmiesLeft(armies)
        elif settingType == "starting_regions":
            noRegion = stdin.readline()
            while(noRegion != ""):
                self.bot.addStartingRegion(noRegion)
                if lineEnds():
                    break
                noRegion = stdin.readline()

    def parseUpdateMap(self):
        self.bot.resetRegionsOwned()
        words = stdin.readline().split(" ")
        while len(words) != 0:
            noRegion = words[0]
            playerName = words[1]
            armies = words[2]
            self.bot.updateRegion(noRegion, playerName, armies)
            if lineEnds():
                break
            words = stdin.readline().split(" ")


    def parseOpponentMoves(self):
        words = stdin.readline().split(" ")
        while len(words) != 0:
            playerName = words[0]
            action = words[1]
            if action == "place_armies":
                move = stdin.readline().split(" ")
                noRegion = move[0]
                armies = move[1]
                self.bot.opponentPlacement(noRegion, armies)
            if action == "attack/transfer":
                move = stdin.readline().split(" ")
                noRegion = move[0]
                toRegion = move[1]
                armies = move[2]
                self.bot.opponentMovement(noRegion, toRegion, armies)
            if lineEnds():
                break

    def parseGo(self):
        words = stdin.readline().split(" ")
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
        words = stdin.readline().split(" ")
        while len(words) != 0:
            superReg = words[0]
            reward = words[1]
            self.bot.addSuperRegion(superReg, reward)
            if lineEnds():
                break
            words = stdin.readline().split(" ")

    def parseRegions(self):
        words = stdin.readline().split(" ")
        while len(words) != 0:
            reg = words[0]
            reward = words[1]
            self.bot.addRegion(reg, reward)
            if lineEnds():
                break
            words = stdin.readline().split(" ")

    def parsePickStartingRegion(self):
        delay = stdin.readline()
        self.bot.startDelay(delay)
        self.bot.clearStartingRegions()
        region = stdin.readline()
        while(region != ""):
            self.bot.addStartingRegion(region)
            if lineEnds():
                break
            region = stdin.readline()
        self.bot.setPhase(self.bot.PICK_STARTING_REGION)

    def parseOpponentStartingRegions(self):
        noRegion = stdin.readline()
        while (noRegion != ""):
            self.bot.addOpponentStartingRegion(noRegion)
            if lineEnds():
                break
            noRegion = stdin.readline()

    def parseNeighbors(self):
        words = stdin.readline().split(" ")
        while(len(words) != 0):
            region = words[0]
            neighbors = words[1]
            neighbors_flds = neighbors.split(",")
            for i in neighbors_flds:
                self.bot.addNeighbors(region, int(i))
            if lineEnds():
                break
            words = stdin.readline().split(" ")

        #TODO:
        #self.bot.setPhase(self.bot.FIND_BORDERS)

    def parseWastelands(self):
        region = stdin.readline()
        while(region != ""):
            self.bot.addWasteland(region)
            if lineEnds():
                break
            region = stdin.readline()