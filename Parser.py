from sys import stdin, stdout

class Parser(object):
    def __init__(self, bot, DEBUG=False):
        self.DEBUG = DEBUG
        self.bot = bot

    def parseInput(self):
<<<<<<< HEAD
        inputType = stdin.readline().strip().split(" ")
        while(len(inputType) != 0):
            if inputType[0] == "setup_map":
                self.parseSetupMap(inputType[1:])
            elif inputType[0] == "settings":
                self.parseSettings(inputType[1:])
            elif inputType[0] == "update_map":
                self.parseUpdateMap(inputType[1:])
            elif inputType[0] == "opponent_moves":
                self.parseOpponentMoves(inputType[1:])
            elif inputType[0] == "pick_starting_region":
                self.parsePickStartingRegion(inputType[1:])
            elif inputType[0] == "go":
                self.parseGo(inputType[1:])
=======
        inputType = stdin.readline().strip()
        if(self.DEBUG): print inputType
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
>>>>>>> origin/master
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
            timebank = inputStr[1]
            self.bot.setTimebank(timebank)
        elif settingType == "time_per_move":
            timePerMove = inputStr[1]
            self.bot.setTimePerMove(timePerMove)
        elif settingType == "max_rounds":
            maxRounds = inputStr[1]
            self.bot.setMaxRounds(maxRounds)
        elif settingType == "your_bot":
            bot_name = inputStr[1]
            self.bot.setBotName(bot_name)
        elif settingType == "opponent_bot":
            bot_name = inputStr[1]
            self.bot.setOpponentBotName(bot_name)
        elif settingType == "starting_armies":
            armies = inputStr[1]
            self.bot.setArmiesLeft(armies)
        elif settingType == "starting_regions":
            noRegions = inputStr[1:]
            for noRegion in noRegions:
                self.bot.addStartingRegion(noRegion)
        elif settyingType == "starting_pick_amount":
            #added by Oz
            amount = inputStr[1]
            self.setStartingPickAmount(amount)

    def parseUpdateMap(self, inputStr):
        self.bot.resetRegionsOwned()
        for i in range(0, len(inputStr), 3):
            noRegion = inputStr[i]
            playerName = inputStr[i+1]
            armies = inputStr[i+2]
            self.bot.updateRegion(noRegion, playerName, armies)

    def parseOpponentMoves(self, inputStr):
        words = inputStr
        i = 0
        while i < len(words):
            playerName = words[i]
            action = words[i+1]
            i += 2
            if action == "place_armies":
                noRegion = words[i]
                armies = words[i+1]
                i += 2
                self.bot.opponentPlacement(noRegion, armies)
            if action == "attack/transfer":
                noRegion = words[i]
                toRegion = words[i+1]
                armies = words[i+2]
                i += 3
                self.bot.opponentMovement(noRegion, toRegion, armies)

    def parseGo(self, inputStr):
        words = inputStr
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

    def parseSuperRegions(self, inputStr):
        words = inputStr
        for i in range(0, len(words), 2):
            superReg = words[i]
            reward = words[i+1]
            self.bot.addSuperRegion(superReg, reward)

    def parseRegions(self, inputStr):
        words = inputStr
        for i in range(0, len(words), 2):
            reg = words[i]
            reward = words[i+1]
            self.bot.addRegion(reg, reward)

    def parsePickStartingRegion(self, inputStr):
        delay = inputStr[0]
        self.bot.startDelay(delay)
        self.bot.clearStartingRegions()
        regions = inputStr[1:]
        for region in regions:
            self.bot.addStartingRegion(region)
        self.bot.setPhase(self.bot.PICK_STARTING_REGION)

    def parseOpponentStartingRegions(self, inputStr):
        noRegions = inputStr
        for noRegion in noRegions:
            self.bot.addOpponentStartingRegion(noRegion)

    def parseNeighbors(self, inputStr):
        words = inputStr
        for i in range(0, len(words), 2):
            region = words[i]
            neighbors = words[i+1]
            neighbors_flds = neighbors.split(",")
            for i in neighbors_flds:
                self.bot.addNeighbors(region, int(i))

        #TODO:
        #self.bot.setPhase(self.bot.FIND_BORDERS)

    def parseWastelands(self, inputStr):
        regions = inputStr
        for region in regions:
            self.bot.addWasteland(region)
