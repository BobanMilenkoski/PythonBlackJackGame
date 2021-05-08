import random
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import sys
from os import path as os_path
from os import system as os_system
import subprocess

def getPossibleHandTotals(hand): 
    totalsList = []
    acelessSum = 0
    aces = 0
    for card in hand:
        if (card.faceValue == 'A'):
            aces += 1
        else:
            acelessSum += card.pointsValue
    if (aces == 0):
        totalsList.append(acelessSum)
    else:
        addAces(totalsList, acelessSum, aces)
    return totalsList

def addAces(totalsList, runningTotal, acesRemaining):
    if (acesRemaining <= 0): 
        pass
    elif (acesRemaining == 1):
        totalsList.append(runningTotal + 1)
        totalsList.append(runningTotal + 11)
    else:
        addAces(totalsList, runningTotal + 1,  acesRemaining-1)
        addAces(totalsList, runningTotal + 11, acesRemaining-1)

def getHandTotalWithinRange(hand, myRange, dealerTurn = False):
    totals = getPossibleHandTotals(hand)
    totals.sort(reverse=True) # Descending order
    if (dealerTurn == False):
        for total in totals:
            if (total in myRange):
                return total
        return 0
    elif (dealerTurn == True):
        for total in totals:
            if (total not in myRange):
                return 0 

def handHasBusted(hand):
   return bool(getHandTotalWithinRange(hand, range(1, 22)) == 0)

def determineHandStatus(hand):
   if handHasBusted(hand):
       return "busted"
   elif ((21 in getPossibleHandTotals(hand)) and (len(hand) == 2)):
       return "blackjack"
   return "stayed"

def settle(playerHand, dealerHand):
    playerStatus = determineHandStatus(playerHand)
    dealerStatus = determineHandStatus(dealerHand)
    whoWon = {'winner': '', 'playerBlackjack': False}
    if (playerStatus == dealerStatus):
        if (playerStatus == "stayed"):
            playerPoints = getHandTotalWithinRange(playerHand, range(4, 22))
            dealerPoints = getHandTotalWithinRange(dealerHand, range(4, 22))
            if (playerPoints > dealerPoints):
                whoWon['winner'] = 'player'
            elif (dealerPoints > playerPoints):
                whoWon['winner'] = 'dealer'
            elif (dealerPoints == playerPoints):
                whoWon['winner'] = 'tie'
        elif (playerStatus == 'busted'):
            whoWon['winner'] = 'dealer'
        else:
           whoWon['winner'] = 'tie'
    elif (playerStatus == "blackjack"):
        whoWon['winner'] = 'player'
        whoWon['playerBlackjack'] = True
    elif (dealerStatus == "blackjack"):
        whoWon['winner'] = 'dealer'
    elif (playerStatus == "busted"):
       whoWon['winner'] = 'dealer'
    elif (dealerStatus == "busted"):
        whoWon['winner'] = 'player'
    else:
        whoWon['winner'] = 'Logic Fallthrough'
    return whoWon
    
class Shoe:
    # a shoe is a container used in casinos to store multiple decks of cards
    # create and contain decks, populate w/cards, shuffle, deal
    def __init__(self, decks):
        self.suits = ["S", "C", "D", "H"]
        self.cardStack = []
        # add calls to addCardToStack here  
        # begin comment out for testhands. add # to the start of each line to comment out.
        for n in range(decks):
            for suit in self.suits:
                for value in range(2, 15):  # values 11-14 are J, K, Q, A respectively
                    if value <= 10:
                        self.cardStack.append(Card(suit, value, value))
                    elif value == 11:
                        self.cardStack.append(Card(suit, "J", 10))
                    elif value == 12:
                        self.cardStack.append(Card(suit, "K", 10))
                    elif value == 13:
                        self.cardStack.append(Card(suit, "Q", 10))
                    elif value == 14:
                        self.cardStack.append(Card(suit, "A", 1))
        # end comment out for testing

    # randomize deck(note: add plastic divider to cut deck)
    def shuffle(self):
        random.shuffle(self.cardStack)
            
    def addCardToStack(self, **kwargs): #testing function to add cards to cardstack. 
        self.cardStack.append(Card(kwargs['suit'], kwargs['cardName'] , kwargs['value']))

    # example function call: self.addCardToStack(suit = 'C', cardName = 10, value = 10)

    # transfer the last card object in the list to indicated hand
    def deal(self, **kwargs):
        # add stack underflow contingency here(prob just reshuffle/recreate)
        for n in range(kwargs['quantity']):
            dealtCard = self.cardStack.pop(0) #return to -1 after test hands
            dealtCard.facing = kwargs['facing']
            kwargs['hand'].append(dealtCard)
        
class Hand(list):
    def __init__(self, name):
        self.name = name
        if self.name == "player":
            self.positionDict = {
                "2": [(500, 308), (674, 308)],
                "3": [(441, 308), (586, 308), (731, 308)],
                "4": [(357, 308), (511, 308), (665, 308), (815, 308)],
                "5": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308)],
                "6": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346)],
                "7": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346)],
                "8": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346)],
                "9": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346)],
                "10": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346), (882, 346)],
                "11": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346), (882, 346), (308, 384)],
                "12": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346), (882, 346), (308, 384), (453, 384)],
                "13": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346), (882, 346), (308, 384), (453, 384), (598, 384)],
                "14": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346), (882, 346), (308, 384), (453, 384), (598, 384), (743, 384)],
                "15": [(296, 308), (441, 308), (586, 308), (731, 308), (876, 308), (302, 346), (447, 346), (592, 346), (737, 346), (882, 346),(308, 384), (453, 384), (598, 384), (743, 384), (888, 384)]
            }
        elif self.name == "dealer":
            self.positionDict = {
                "2": [(500, 68), (674, 68)],
                "3": [(441, 68), (586, 68), (731, 68)],
                "4": [(357, 68), (511, 68), (665, 68), (815, 68)],
                "5": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68)],
                "6": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (312, 87)],
                "7": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (312, 87), (457, 87)],
                "8": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (302, 87), (457, 87), (602, 87)],
                "9": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (302, 87), (457, 87), (602, 87), (747, 87)],
                "10": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (302, 87), (457, 87), (602, 87), (747, 87), (892, 87)],
                "11": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (302, 87), (457, 87), (602, 87), (747, 87), (892, 87), (328, 106)],
                "12": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (302, 87), (457, 87), (602, 87), (747, 87), (892, 87), (328, 106), (453, 106)],
                "13": [(296, 68), (441, 68), (586, 68), (731, 68), (876, 68), (302, 87), (457, 87), (602, 87), (747, 87), (892, 87), (328, 106), (453, 106), (598, 106)]
            }

class Card:
    def __init__(self, suit, faceVal, pointsVal):
        self.suit = suit
        self.faceValue = faceVal
        self.pointsValue = pointsVal
        self.x = 0
        self.y = 0
        self.facing = "up"
        self.name = str(self.faceValue) + self.suit

class Session:
    def __init__(self):
        self.root = Tk()
        self.root.title("OakJack")
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.isMenuRunning = False
        self.playerWallet = 100
        self.cardPhotoImages = {}
        for suit in ['C','H','D','S']:
            for i in range(1, 14):
                try:
                    face = {1 : 'A', 11: 'J', 12: 'Q', 13: 'K'}[i]
                except KeyError as E:
                    face = str(i)
                fname = face + suit
                ext = ".png"
                cardFileName = face + suit + ext
                self.cardPhotoImages[fname] = PhotoImage(file = os_path.join('Assets', 'cards_png_zip', cardFileName))
        self.cardPhotoImages['back'] = PhotoImage(file = os_path.join('Assets', 'cards_png_zip', 'red_back.png'))

    def run(self):
        self.initMenuUIElements()  
        self.root.mainloop()

    def initMenuUIElements(self):
        self.menuFrame = Frame(master=self.root)
        self.menuFrame.grid(row=0, column=0, sticky = 'EWNS')

        self.menuFrame.grid_columnconfigure(0, weight = 1)
        self.menuFrame.grid_rowconfigure(0, weight = 1)

        self.cardTableImg = PhotoImage(file = os_path.join('Assets', 'startScreen.png'))
        self.cardTableCanvas = Canvas(master = self.menuFrame, bd = 0, highlightthickness = 0)
        self.cardTableCanvas.create_image(0, 0, image=self.cardTableImg, anchor='nw')
        self.cardTableCanvas.grid(row = 0, column = 0, sticky = 'EWNS', rowspan = 4)

        self.menuButtonSize = PhotoImage(width = 160, height = 160)

        startButtonCallback = self.initGame
        self.startButton = Button(master = self.menuFrame, text = "Start Game", image = self.menuButtonSize, compound = "c", command = startButtonCallback)
        self.startButtonWindow = self.cardTableCanvas.create_window(1100, 100, anchor = "nw", window = self.startButton)

        helpButtonCallback = self.openHelp
        self.helpButton = Button(master = self.menuFrame, text = "Help/Game Info", image = self.menuButtonSize, compound = "c", command = helpButtonCallback)
        self.helpButtonWindow = self.cardTableCanvas.create_window(1100, 300, anchor = "nw", window = self.helpButton)

        endButtonCallback = sys.exit
        self.endButton = Button(master = self.menuFrame, text = "Quit Game", image = self.menuButtonSize, compound = "c", command = endButtonCallback)
        self.endButtonWindow = self.cardTableCanvas.create_window(1100, 500, anchor = "nw", window = self.endButton)

    def openHelp(self):
        subprocess.Popen("HelpSection.pdf", shell = True)

    def initGame(self):
        self.pot = 0
        self.playerHand = Hand("player")
        self.playerPoints = 0
        self.dealerHand = Hand("dealer")
        self.dealerPoints = 0
        self.bet = 0
        self.shoe = Shoe(2)
        self.cardDict = {'player':{}, 'dealer':{}}
        self.initBetUIElements()
      
    def initBetUIElements(self):
        self.betFrame = Frame(master = self.root)
        self.betFrame.grid(row = 0, column = 0, sticky = "EWNS")

        self.betFrame.grid_columnconfigure(0, weight = 1)
        self.betFrame.grid_rowconfigure(0, weight = 1)

        self.cardTableCanvas = Canvas(master = self.betFrame, bd = 0, highlightthickness = 0)
        self.cardTableCanvas.create_image(0, 0, image = self.cardTableImg, anchor = "nw")
        self.cardTableCanvas.grid(row = 0, column = 0, sticky = "EWNS")

        betButtonCallback = self.checkBet
        self.betButton = Button(master = self.betFrame, text = "Place Your Bet!", image = self.menuButtonSize, compound = "c", command = betButtonCallback)
        self.betButtonWindow = self.cardTableCanvas.create_window(560, 400, anchor = "nw", window = self.betButton)

        self.totalChipDisplay = Text(master = self.betFrame, pady = 20, background = "white", foreground = "black", width = 8, height = 1, font = ("Arial", 31))
        self.tcdWindow = self.cardTableCanvas.create_window(400, 200, anchor = "nw", window = self.totalChipDisplay)
        self.totalChipDisplay.insert(1.0, str(self.playerWallet))
        self.totalChipDisplay["state"] = "disabled"

        self.totalLabel = Label(master = self.betFrame, background = "green", text = "Total Chips:", font = ("Arial", 27))
        self.totalLabelWindow = self.cardTableCanvas.create_window(400, 100, anchor = "nw", window = self.totalLabel)

        self.currentBetDisplay = Text(master = self.betFrame, pady = 20, background = "white", foreground = "black", width = 8, height = 1, font = ("Arial", 31))
        self.cbdWindow = self.cardTableCanvas.create_window(693, 200, anchor = "nw", window = self.currentBetDisplay)

        self.betLabel = Label(master = self.betFrame, background = "green", text = "Input Bet:", font = ("Arial", 27))
        self.betLabelWindow = self.cardTableCanvas.create_window(693, 100, anchor = "nw", window = self.betLabel)

        self.responseLabel = Label(master = self.betFrame, background = "green", text = "", font = ("Arial", 27))
        self.responseLabelWindow = self.cardTableCanvas.create_window(693, 300, anchor = "nw", window = self.responseLabel)

    def gameStateInit(self):
        self.shoe.shuffle()
        self.initGameUIElements()
        self.shoe.deal(hand = self.playerHand, quantity = 2, facing = "up")
        self.shoe.deal(hand = self.dealerHand, quantity = 1, facing = "up")
        self.shoe.deal(hand = self.dealerHand, quantity = 1, facing = "down")
        self.decideCardLayout(self.playerHand)
        self.decideCardLayout(self.dealerHand)
        if (determineHandStatus(self.playerHand) == 'blackjack' or determineHandStatus(self.dealerHand) == 'blackjack'):
            self.updateButtonStatus(hand = self.playerHand, button = self.hitButton, cardDealt = True)
            self.updateButtonStatus(hand = self.playerHand, button = self.doubleButton)
        else:
            self.updateButtonStatus(hand = self.playerHand, range = range(4, 21), button = self.hitButton, cardDealt = True)
            if self.playerWallet >= self.bet:
                self.updateButtonStatus(hand = self.playerHand, range = range(9, 12), button = self.doubleButton)
            else:
                self.updateButtonStatus(hand = self.playerHand, button = self.doubleButton)

    def updateButtonStatus(self, **kwargs):
        if 'cardDealt' not in kwargs.keys():
            kwargs['cardDealt'] = False
        if 'range' not in kwargs.keys():
            kwargs['range'] = range(0, 1)
        currentHandPoints = getHandTotalWithinRange(kwargs['hand'], kwargs['range'])
        if (currentHandPoints == 0):
            kwargs['button']['state'] = "disabled"
            if (kwargs['cardDealt'] == True):
                self.flashUIButton()

    def flashUIButton(self):
        style1 = Style()
        style1.configure("A.TButton", background = "#FF0000")
        style2 = Style()
        style2.configure("B.TButton", background = "#FFFF00")
        self.count = 8
        def f1():
            self.stayButton.config(style="A.TButton")
            self.stayButton['text'] = 'Continue to Dealer'
            if (self.count > 0):
                self.count -= 1
                self.root.after(333, f2)
        def f2():
            self.stayButton.config(style="B.TButton")
            if (self.count > 0):
                self.count -= 1
                self.root.after(333, f1)
        self.root.after(333, f1)
            
    def checkBet(self):
        try:
            inputBet = int(self.currentBetDisplay.get(1.0, "end-1c"))
            if (inputBet <= self.playerWallet and inputBet > 0):
                self.bet = inputBet
                self.pot = inputBet * 2
                self.playerWallet -= inputBet
                self.responseLabel["text"] = ("Bet successful!\nThe pot will be: " + str(self.pot))
                self.root.after(1500, self.gameStateInit)
            elif (inputBet > self.playerWallet):
                self.responseLabel["text"] = "You do not have that many chips.\nPlease input another value."
                self.currentBetDisplay.delete(1.0, 2.0)
            elif (inputBet < 0):
                self.responseLabel["text"] = "Negative chip amounts are not accepted.\nPlease input another value."
                self.currentBetDisplay.delete(1.0, 2.0)
            else:
                self.responseLabel["text"] = "OK but literally how tho"
                self.currentBetDisplay.delete(1.0, 2.0)

        except ValueError:
            self.responseLabel["text"] = "This is not a number.\nPlease input a valid number."
            self.currentBetDisplay.delete(1.0, 2.0)

    def initGameUIElements(self):
        self.gameFrame = Frame(master=self.root)
        self.gameFrame.grid(row=0, column=0, sticky = 'EWNS')

        self.gameFrame.grid_columnconfigure(0, weight = 1)
        self.gameFrame.grid_rowconfigure(0, weight = 1)

        self.gameTableImg = PhotoImage(file = os_path.join('Assets', 'gameScreen.png'))
        self.cardTableCanvas = Canvas(master = self.gameFrame, bd = 0, highlightthickness = 0)
        self.cardTableCanvas.create_image(0, 0, image=self.gameTableImg, anchor='nw')
        self.cardTableCanvas.grid(row = 0, column = 0, sticky = 'EWNS', rowspan = 4)

        self.chipBoxImg = PhotoImage(file = os_path.join('Assets', 'chipbox.png'))
        self.chipBoxWindow = self.cardTableCanvas.create_image(0, 0, image = self.chipBoxImg, anchor = "nw")

        self.totalChipDisplay = Text(master = self.gameFrame, pady = 20, background = "black", foreground = "white", width = 7, height = 1, font = ("Arial", 31))
        self.tcdWindow = self.cardTableCanvas.create_window(13, 48, anchor = "nw", window = self.totalChipDisplay)
        self.totalChipDisplay.insert(1.0, str(self.playerWallet))
        self.totalChipDisplay['state'] = 'disabled'

        self.currentPotDisplay = Text(master = self.gameFrame, pady = 20, background = "black", foreground = "white", width = 7, height = 1, font = ("Arial", 31))
        self.cpdWindow = self.cardTableCanvas.create_window(13, 170, anchor = "nw", window = self.currentPotDisplay)
        self.currentPotDisplay.insert(1.0, str(self.pot))
        self.currentPotDisplay['state'] = 'disabled'

        self.gameButtonSize = PhotoImage(width = 160, height = 80)

        hitButtonCallback = self.hitPhase
        self.hitButton = Button(master = self.gameFrame, text = "Hit", image = self.gameButtonSize, compound = "c", command = hitButtonCallback)
        self.hitButtonWindow = self.cardTableCanvas.create_window(233, 617, anchor = "nw", window = self.hitButton)

        stayButtonCallback = self.disableDealButtons
        self.stayButton = Button(master = self.gameFrame, text = "Stay", image = self.gameButtonSize, compound = "c", command = stayButtonCallback)

        self.stayButtonWindow = self.cardTableCanvas.create_window(560, 617, anchor = "nw", window = self.stayButton)

        doubleButtonCallback = self.doubleDownPhase
        self.doubleButton = Button(master = self.gameFrame, text = "Double\nDown", image = self.gameButtonSize, compound = "c", command = doubleButtonCallback)
        self.doubleButtonWindow = self.cardTableCanvas.create_window(876, 617, anchor = "nw", window = self.doubleButton)

        self.quitButtonSize = PhotoImage(width=150, height=50)
        quitButtonCallback = self.quitHand
        self.quitButton = Button(master = self.gameFrame, text = "Quit Hand", image = self.quitButtonSize, compound = "c", command = quitButtonCallback)
        self.quitButtonWindow = self.cardTableCanvas.create_window(1115, 5, anchor = "nw", window = self.quitButton)

    def disableDealButtons(self):
        self.updateButtonStatus(hand = self.playerHand, button = self.hitButton)
        self.updateButtonStatus(hand = self.playerHand, button = self.doubleButton)
        self.dealerTurn()

    def hitPhase(self):
        self.shoe.deal(hand = self.playerHand, quantity = 1, facing = "up")
        self.decideCardLayout(self.playerHand)
        self.updateButtonStatus(hand = self.playerHand, range = range(4, 21), button = self.hitButton, cardDealt = True)
        self.updateButtonStatus(hand = self.playerHand, button = self.doubleButton)

    def doubleDownPhase(self):
        self.playerWallet -= self.bet
        self.bet *= 2
        self.pot *= 2
        self.shoe.deal(hand = self.playerHand, quantity = 1, facing = "down")
        self.decideCardLayout(self.playerHand)
        self.updateTextDisplay(self.totalChipDisplay, self.playerWallet)
        self.updateTextDisplay(self.currentPotDisplay, self.pot)
        self.updateButtonStatus(hand = self.playerHand, button = self.doubleButton, cardDealt = True)
        self.updateButtonStatus(hand = self.playerHand, button = self.hitButton)

    def dealerTurn(self):
        self.turnCardsUp()
        if (determineHandStatus(self.dealerHand) == 'blackjack' or determineHandStatus(self.playerHand) == 'busted'):
            pass
        else:
            currentDealerTotal = getHandTotalWithinRange(self.dealerHand, range(4, 17), True)
            while (currentDealerTotal != 0):
                self.shoe.deal(hand = self.dealerHand, quantity = 1, facing = "up")
                currentDealerTotal = getHandTotalWithinRange(self.dealerHand, range(4, 17), True)
            self.decideCardLayout(self.dealerHand)
        self.decideCardLayout(self.dealerHand)
        self.root.after(5000, self.settleHand)

    def turnCardsUp(self):
        for card in self.playerHand:
            card.facing = 'up'
        for card in self.dealerHand:
            card.facing = 'up'
        self.decideCardLayout(self.playerHand)
        self.decideCardLayout(self.dealerHand)
            
    def updateTextDisplay(self, text, newValue):
        text['state'] = 'normal'
        text.delete(1.0, 2.0)
        text.insert(1.0, str(newValue))
        text['state'] = 'disabled'

    def initResultsUIElements(self, winnerDict):

        self.resultsFrame = Frame(master = self.root)
        self.resultsFrame.grid(row = 0, column = 0, sticky = 'EWNS')

        self.resultsFrame.grid_columnconfigure(0, weight = 1)
        self.resultsFrame.grid_rowconfigure(0, weight = 1)

        self.cardTableImg = PhotoImage(file = os_path.join('Assets', 'startScreen.png'))
        self.cardTableCanvas = Canvas(master = self.resultsFrame, bd = 0, highlightthickness = 0)
        self.cardTableCanvas.create_image(0, 0, image = self.cardTableImg, anchor = "nw")
        self.cardTableCanvas.grid(row = 0, column = 0, sticky = "EWNS")

        self.menuButtonSize = PhotoImage(width = 160, height = 160)

        resultLabelText = ''
        if (winnerDict['winner'] == 'player'):
            resultLabelText = 'Congratulations, you won!\nYour new total chips are: '
        elif (winnerDict['winner'] == 'dealer'):
            resultLabelText = 'Tough break, you lost.\nHere\'s how many chips you have left: '
        elif (winnerDict['winner'] == 'tie'):
            resultLabelText = "That game was a wash!\nHere's your chips back: "
        else:
            print("ResultsLabel Logic Error")

        self.resultLabel = Label(master = self.resultsFrame, text = resultLabelText, background = 'green', font = ('Arial', 21))
        self.resultLabelWindow = self.cardTableCanvas.create_window(100, 200, anchor = 'nw', window = self.resultLabel)

        self.totalChipDisplay = Text(master = self.resultsFrame, pady = 20, background = "black", foreground = "white", width = 7, height = 1, font = ("Arial", 31))
        self.tcdWindow = self.cardTableCanvas.create_window(720, 175, anchor = 'nw', window = self.totalChipDisplay)
        self.updateTextDisplay(self.totalChipDisplay, self.playerWallet)


        newHandButtonCallback = self.initGame  
        self.newHandButton = Button(master = self.resultsFrame, text = '   Start a\nnew hand!', image = self.menuButtonSize, compound = 'c', command = newHandButtonCallback)
        self.newHandButtonWindow = self.cardTableCanvas.create_window(320, 300, anchor = 'nw', window = self.newHandButton)

        returnToMenuCallback = self.quitHand
        self.returnToMenuButton = Button(master = self.resultsFrame, text = '             Return to\n             Main Menu.\n(Total Chips are not saved)', image = self.menuButtonSize, compound = 'c', command = returnToMenuCallback)
        self.returnToMenuButtonWindow = self.cardTableCanvas.create_window(720, 300, anchor = 'nw', window = self.returnToMenuButton)


    def settleHand(self): #compare the player and dealer point values, as well as number of cards in hand, to determine outcome
        winnerDict = settle(self.playerHand, self.dealerHand)
        if (winnerDict['winner'] == 'player' and winnerDict['playerBlackjack'] == True):
            self.pot += self.bet * 0.5
            self.playerWallet += self.pot
        elif (winnerDict['winner'] == 'player'):
            self.playerWallet += self.pot
        elif (winnerDict['winner'] == 'tie'):
            self.playerWallet += self.bet
        elif (winnerDict['winner'] == 'dealer'):
            pass
        else:
            print('Logical Error')
        
        if (self.playerWallet == 0):
            self.outOfChips()
        else:
            self.initResultsUIElements(winnerDict)

    def outOfChips(self):
        messagebox.showinfo("Casino Guards", "Sorry buddy, you lost, better luck next time.\nYou're out of chips!")
        self.quitHand()

    def quitHand(self):
        self.playerWallet = 100
        self.initMenuUIElements()

    def decideCardLayout(self, hand): #takes how many cards each hand has and assigns proper positional data to them for rendering
        handCardPositions = hand.positionDict[str(len(hand))]
        for i in range(0, len(hand)):
            hand[i].x = handCardPositions[i][0]
            hand[i].y = handCardPositions[i][1]
        
        keys = self.cardDict[hand.name].keys()
        if (len(keys) > 0):
            for key in keys:
                self.cardDict[hand.name][key]['label'].destroy()
            self.cardDict[hand.name] = {}
        for card in hand:
            i = len(self.cardDict[hand.name])
            self.cardDict[hand.name][i] = {}
            if (card.facing == 'down'):
                self.cardDict[hand.name][i]['label'] = Label(master = self.gameFrame, image = self.cardPhotoImages['back'])
            else:
                self.cardDict[hand.name][i]['label'] = Label(master = self.gameFrame, image = self.cardPhotoImages[card.name])
            self.cardDict[hand.name][i]['window'] = self.cardTableCanvas.create_window(card.x, card.y, anchor = "nw", window = self.cardDict[hand.name][i]['label'])      


gameSesh = Session()
gameSesh.run()