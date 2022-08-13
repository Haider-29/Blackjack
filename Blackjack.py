#Syed Haider Naqvi, Japmeet Bedi, Kara Walp
#PA 5
#14th November, 2020
#This program runs a game of blackjack

from operator import itemgetter
import sys
from graphics import *
from random import *
#Imports the required modules


class Button:

    """A button is a labeled rectangle in a window.
    It is enabled or disabled with the activate()
    and deactivate() methods. The clicked(pt) method
    returns True if and only if the button is enabled and pt is inside it."""

    def __init__(self, win, center, width, height, label):


        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """
        
        self.win = win
        #Saves the graphic window upon which the button will be drawn to a variable
        
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w 
        self.ymax, self.ymin = y+h, y-h
        #Calculates middle points and edge points for the buttons
        
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        #Saves those points in the form of point objects
        
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('red')
        self.rect.draw(win)
        #Creates and draws the rectangle part of the button
        
        self.label = Text(center, label)
        self.label.draw(win)
        #Creates and draws the label part of the button
        
        self.activate()
        #Starts off the button as activated

    def getLabel(self):
        
        """Returns the label string of this button."""
        
        return self.label.getText()

    def activate(self):
        
        """Sets this button to 'active'."""
        
        self.label.setFill('black') 
        self.rect.setWidth(2)       
        self.active = True
        #Sets label fill to black, makes the rectangle have a thicker boundary 
        #and activates it
        
    def deactivate(self):
        
        """Sets this button to 'inactive'."""
        
        self.label.setFill('darkgray')  
        self.rect.setWidth(1)           
        self.active = False
        #Sets the label fill to gray, makes the rectangle have a thinner boundary
        #and deactivates it

    def isClicked(self, pt):
        
        """Returns true if button active and Point pt is inside"""
        
        if self.active == True:
            if  (self.xmin <= pt.getX() <= self.xmax) and (self.ymin <= pt.getY() <= self.ymax): 
                return True
            else:
                return False
        #Checks if the click is inside the dimensions of the button and then
        #returns a True or False Boolean 

    def setSize(self, size):
        
        """Sets the size of the text in the label to a user specified size"""
        
        self.label.setSize(size)

    def unDraw(self):
        
        """Undraws and deactivates the button"""
        
        self.rect.undraw()
        self.label.undraw()
        self.deactivate()

    def Draw(self):
        
        """Draws and activates the button"""
        
        self.rect.draw(self.win)
        self.label.draw(self.win)
        self.activate()

    def setLabel(self, label):
        
        """Sets the text of the label to a user specified text"""
        
        self.label.setText(label)
        
        
class PlayingCard():

    """A playing card is simply a rank from 1 to 13 alongside a suit"""
    
    def __init__(self, rank, suit):
        
        """Creates a playing card with a rank between 1 and 11 and a suit
            of either clubs, hearts, spades, or diamonds"""
        
        self.rank = rank
        self.suit = suit
        self.card = [rank,suit]

    def getRank(self):
        
        """Returns the rank of the specified playing card"""
        
        return self.rank

    def getSuit(self):
        
        """Returns the suit of the specified playing card"""
        
        return self.suit

    def value(self):
        
        """Converts the rank of the card into its face value"""
        
        if self.rank == 1:
            return 11

        if self.rank >= 2 and self.rank <= 10:
            return self.rank

        if self.rank >= 11 and self.rank <= 13:
            return 10

    def __str__(self):
        
        """Converts the rank and suit of the card into a string
            of text of the format rank of suit and returns that"""
        
        list_of_cards = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", \
                         "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        #Initialises the possible cards into a list
        
        for i in range(len(list_of_cards)):
            if self.rank == i + 1:
                card_name = list_of_cards[i]
        #Figures out the numerical name of the card and saves it to a variable

        suit_of_cards = ["Diamonds", "Clubs","Hearts","Spades"]
        letter_of_suits = ["d", "c", "h", "s"]
        #Initialises the possible suits into a list alongside their abbreviations
        #which are used to refer to the suits

        for letter in range(len(letter_of_suits)):
            if self.suit == letter_of_suits[letter]:
                card_suit = suit_of_cards[letter]
        #Figures out the suit of the card and saves it to a variable

        name_of_card = card_name + " of " + card_suit
        #Creates the name of the card

        return name_of_card
        #Returns the name of the card

class Deck():

    """A deck is a collection of playing cards which can be shuffled, dealt, etc"""

    def __init__(self):
        
        """Initialises s standard deck by dealing out 13 cards of
            4 suits for a total of 52 cards"""
        
        self.cards_in_deck = []
        suits = ["d", "h", "s", "c"]
    
        for suit in range(4):
            for rank in range(1,14):
                card = PlayingCard(rank, suits[suit])
                self.cards_in_deck.append(card)
        #Creates a deck by iterating through the 4 different suits for 13 cards each

    def shuffle(self):
        
        """Randomises the order of the cards in the deck"""
        
        return(shuffle(self.cards_in_deck))

    def dealCard(self):
        
        """Deals a card from the deck and removes it"""
        
        return(self.cards_in_deck.pop(0))

    def cardsLeft(self):
        
        """Returns the number of cards left in the deck"""
        
        return(len(self.cards_in_deck))


class Blackjack():

    """A game of blackjack is played through this class. It includes
        all the functions including dealing cards,evaluating hand values,
        drawing the game on the graphics GUI and more"""

    def __init__(self, d_hand = [], p_hand = []):
        
        """Initialises the game by creating a deck and shuffling it and
            creating an empty player and dealer hand"""
        
        self.deck = Deck()
        self.deck.shuffle()
        #Creates the deck to be used for the game and shuffles it
        
        self.d_hand = d_hand
        self.p_hand = p_hand
        #Saves the dealer and player hands as empty lists initially

    def initDeal(self, gwin, xposD, yposD, xposP, yposP):
        
        """Deals two cards each per player and dealer and draws them
            onto the graphics window"""
        
        self.d_hand, self.p_hand = [],[]
        #Saves dealer and player hands as empty lists so that when main() is
        #called recursively, the old hands do not overlap with the new ones
        
        for i in range(2):
            card = self.deck.dealCard()
            self.d_hand.append(card)
        #Deals two cards to the dealer

            if i == 0:
                if card.getSuit() == "h" or card.getSuit() == "d":
                    card_image = Image(Point(xposD,yposD), "playingcards/b2fv.gif")
                    card_image.draw(gwin)
                    xposD = xposD + 5
                else:
                    card_image = Image(Point(xposD,yposD), "playingcards/b1fv.gif")
                    xposD = xposD + 5
                    card_image.draw(gwin)
            #Draws the dealers first card face down onto the GUI
                                

            if i == 1:
                card_file_name = "playingcards/" + str(card.getSuit()) + str(card.getRank()) + ".gif"
                card_image = Image(Point(xposD,yposD), card_file_name)
                card_image.draw(gwin)
                xposD = xposD + 5
            #Draws the next card normally

            
        for i in range(2):
            card = self.deck.dealCard()
            self.p_hand.append(card)
            card_file_name = "playingcards/" + str(card.getSuit()) + str(card.getRank()) + ".gif"
            card_image = Image(Point(xposP,yposP), card_file_name)
            card_image.draw(gwin)
            xposP = xposP + 5
        #Draws both cards of the player onto the GUI normally
        

        return self.d_hand, self.p_hand
        #Returns both the players hand and the dealers hand

    def hit(self, gwin, xPos, yPos):
        
        """Deals a card to the player and removes it from the deck"""
        
        card = self.deck.dealCard()
        self.p_hand.append(card)
        #Deals a card to the player and appends it to the player hand
        
        card_file_name = "playingcards/" + str(card.getSuit()) + str(card.getRank()) + ".gif"
        card_image = Image(Point(xPos, yPos), card_file_name)
        card_image.draw(gwin)
        #Draws the card onto the GUI
        
        return self.p_hand
        #Returns the new value of the player hand

    def evaluateHand(self, hand):
        
        """Evaluates the face value of the user specified hand and
            returns its value"""
        
        hand_total = 0
        #Initialises the hand value as 0

        ace_count = self.hasAce(hand)
        #Counts the number of Aces that a hand has
    
        for card in range(len(hand)):
            hand_total = hand_total + hand[card].value()
        #Finds the value of the hand

        while hand_total > 21 and ace_count > 0:
            hand_total = hand_total - 10
            ace_count = ace_count - 1
        #Converts the value of Aces from 11 to 1 if needed according to the number
        #of Aces that the user has

        return hand_total
        #Returnt the value of the hand

    def dealerPlays(self, gwin, xPos, yPos):
        
        """Deals more cards to the dealer if his total is below 17 and
            evaluates his total and returns it after dealer hand value is over 17"""
        
        dealer_total = self.evaluateHand(self.d_hand)

        while dealer_total < 17:

            card = self.deck.dealCard()
            self.d_hand.append(card)
            dealer_total = self.evaluateHand(self.d_hand)
        #Evaluated the value of the dealers hand, and if it is less than 17 keeps
        #hitting the dealer until his value is above 17

        for card in range(len(self.d_hand)):

            card_file_name = "playingcards/" + str(self.d_hand[card].getSuit()) + \
            str(self.d_hand[card].getRank()) + ".gif"
            card_image = Image(Point(xPos,yPos), card_file_name)
            card_image.draw(gwin)
            xPos = xPos + 5
        #Draws all the dealers cards onto the GUI again, including the one
        #which was face down initially which will be face up now

        return dealer_total
        #Returns the value of the dealers hand

    def hasAce(self, hand):
        
        """Returns how many aces are in a specific hand"""
        
        ace_count = 0

        for card in range(len(hand)):
            if hand[card].getRank() == 1:
                ace_count = ace_count + 1
        #Counts the number of aces in a hand and saves it to a variable

        return ace_count
        #Returns the value to the program

class Bank():

    """A bank is an object which simply stores the amount of money the person
        currently has in his pool and allows us to subtract lost bets, add won
        bets, and draw it all on the graphic interface. It also keeps track
        of the highscores earned by players of the game with their names"""

    def __init__(self, win, xPos, yPos, filename_money, filename_highscore):
        
        """Initialises the starting amount of money in the players bank,
            reads the highscore list from the txt file, and draws the amount
            of money in the users bank on the top right of the graphics window"""
        
        self.filename_money = filename_money
        self.moneyfile = open(filename_money, "r")
        self.bank = int(self.moneyfile.readline())
        #Opens the file storing the initial amount of money the player has in
        #read mode and saves the amount to a variable
        
        self.xPos = xPos
        self.yPos = yPos
        self.win = win
        #Saves the window and the position where the bank must be drawn on the GUI
        
        self.filename_highscore = filename_highscore
        self.scorefile = open(filename_highscore, "r")
        self.listOfScoresAndNames = self.scorefile.read().split("\n")
        #Opens the highscores file and reads the current highscores into
        #a list of name and score seperared by name
        
        self.list_tuples = []
        #Initialises the list where the names and highscores will be stored as tuples
        
        for item in range(len(self.listOfScoresAndNames)- 1):
            name, score = self.listOfScoresAndNames[item].split()
            self.list_tuples.append((name,int(score)))
        #Saves the names and highscores of the users into a list of tuples 
            
        self.bet_bank = Button(self.win, Point(self.xPos,self.yPos), 10, 5, "$" + str(self.bank))
        #Draws the current amount the user has in the bank onto the GUI

    def currentAmount(self):
        
        """Returns the current amount of money in the users bank"""
        
        return self.bank

    def isBroke(self):
        
        """Checks if the user is broke and returns a boolean True or False"""
        
        if self.bank <= 0:
            return True
        else:
            return False

    def betLost(self, bet):
        
        """Subtracts money from the users bank if they lose a bet and
            updates the GUI with new amount"""
        
        moneyfilewrite = open(self.filename_money, "w")
        #Opens the file where the bank value is stored in write mode
        
        self.bank = int(self.bank) - bet
        #Updates the value of the bank

        if self.bank < 0:
            self.bank = 0
        #In the case where player goes all in and loses to dealer blackjack,
        #this will prevent bank from going into a negative number
        
        self.bet_bank.setLabel("$" + str(self.bank))
        #Updates the value of the bank on the GUI
        
        moneyfilewrite.write(str(self.bank))
        #Writes the new bank value onto the text file

    def betWon(self, bet):
        
        """Adds money to the users bank if they win a bet and
            updates the GUI with new amonut"""
        
        moneyfilewrite = open(self.filename_money, "w")
        #Opens the file where the bank value is stored in write mode
        
        self.bank = int(self.bank) + bet
        #Updates the value of the bank
        
        self.bet_bank.setLabel("$" + str(self.bank))
        #Updates the value of the bank on the GUI
        
        moneyfilewrite.write(str(self.bank))
        #Writes the new bank value onto the text file
        

    def highScores(self):
        
        """Returns the current list of highscores with their respective names"""
        
        return self.list_tuples

    def isHighscore(self, score):
        
        """Checks if the current score is a highscore and
            returns a boolean True or False"""
        
        for i in range(len(self.list_tuples)):

            if score > self.list_tuples[i][1]:
                return True
            
        return False

    def newHighscore(self, name, score):
        
        """Adds a new highscore to the list, sorts it according to the
            highest scores, limits it to 5 entries, and saves it to the
            txt file where the highscores are stored"""
        
        self.list_tuples.append((name ,score))
        self.list_tuples = sorted(self.list_tuples, key = itemgetter(1), reverse = True)[:5]
        #Adds the new highscore and name to the list, sorts it by highscore, and
        #restricts the list to 5 items

        scorefile_write = open(self.filename_highscore, "w")
        #Opens the highscores list in write mode
        
        for item in range(len(self.list_tuples)):
            scorefile_write.write(str(self.list_tuples[item][0]) + " " + \
            str(self.list_tuples[item][1]) + "\n")
        scorefile_write.close()
        #Writes the new highscores onto the text file and closes the file to save it

    def drawHighscores(self):
        
        """Draws the highscores on the GUI"""
        
        xPos_name = 30
        xPos_score = 70
        yPos = 80
        #initialises the position of the first high score and name to be
        #drawn onto the GUI

        highscore = Button(blackjack, Point(50,93), 30,10, "Highscores")
        highscore.setSize(25)
        #Creates a highscore title

        close_button = Button(blackjack, Point(50,7), 95,10, "Please click anywhere to exit the game")
        close_button.setSize(25)
        #Creates a button which prompts the user to click anywhere to
        #close the game

        for i in range(len(self.list_tuples)):

            name = Button(blackjack, Point(xPos_name, yPos), 20,10 , str(self.list_tuples[i][0]))
            name.setSize(25)
            
            score = Button(blackjack, Point(xPos_score, yPos), 20,10, str(self.list_tuples[i][1]))
            score.setSize(25)

            yPos = yPos - 15
            
        #Draws all the highscores onto the GUI, updating the position
        #of each highscore and name each time


def checkHighscore():

    if bank.isHighscore(bank.currentAmount()):
    #Checks if the users score is a highscore before letting them quit

        clearScreen()
        highscore_button = Button(blackjack, Point(50,70), 80,20, \
        "You got a new highscore!\nPlease enter your first name and\nclick continue to save it")
        highscore_button.setSize(25)
        #If the score is a highscore, informs the user of that and asks for
        #their name so it can be saved to the list of highscores

        name_entry = Entry(Point(50,30), 30)
        name_entry.draw(blackjack)
        #Creates an entry box where the name is to be entered

        continue_button.Draw()
        continue_click = blackjack.getMouse()
        #Creates the continue button which the user must click and checks
        #for a mouseclick

        while not continue_button.isClicked(continue_click):
            continue_click = blackjack.getMouse()
        #Keeps checking for a mouseclick until the user clicks the
        #continue button

        name = str(name_entry.getText())
        #Saves the name that the user enters to a variable

        name_entry.undraw()
        #Undraws the entry box

        bank.newHighscore(name, bank.currentAmount())
        #Adds the new highscore to the list of highscores and
        #saves it to the text file

def endGame():

    clearScreen()
    highscore_ask = Button(blackjack, Point(50,70), 70,20, \
    "Would you like to see the\nhighscores before quitting?")
    highscore_ask.setSize(25)
    #Asks the user if they would like to see the highscores before quitting

    yes_button = Button(blackjack, Point(30,30), 10,10, "Yes")
    yes_button.setSize(25)
    no_button = Button(blackjack, Point(70,30), 10, 10, "No")
    no_button.setSize(25)
    #Draws the yes or no buttons
    
    yes_or_no = blackjack.getMouse()
    while not yes_button.isClicked(yes_or_no) and not no_button.isClicked(yes_or_no):
        yes_or_no = blackjack.getMouse()
    #Waits for a mouselick and keeps waiting for a mouselick until one
    #of the buttons is clicked

    if yes_button.isClicked(yes_or_no):
    #Checks if the user clicked yes

        clearScreen()
        bank.drawHighscores()
        blackjack.getMouse()
        #If the user clicked yes, shows them the highscores of the game
        #before prompting them to click anywhere to exit the game

    
    newfile = open("money.txt", "w")
    newfile.write("5000")
    newfile.close()
    #Resets the amount of money in the bank back to 5000,
    #which is the initial amount
    
    blackjack.close()
    #Closes the blackjack GUI

            
def clearScreen():

    background = Rectangle(Point(0,0),Point(100,100))
    background.setFill("green")
    background.draw(blackjack)
    #Clears the screen of all buttons by drawing over it
    #with a solid green background

  
def main():

    global blackjack
    blackjack = GraphWin("Blackjack", 600, 600)
    #Creates the graphics window and defines it to be a global variable

    blackjack.setCoords(0,0,100,100)
    #Sets the coordinate system of the GUI to be a
    #100 x 100 coordinate system for easier drawing 

    background = Rectangle(Point(0,0),Point(100,100))
    background.setFill("green")
    background.draw(blackjack)
    #Draws a green background

    blackjack_title = Button(blackjack, Point(50,90), 50,10,"Blackjack!")
    blackjack_title.setSize(25)
    #Draws the blackjack title

    hit_button = Button(blackjack, Point(30,10), 20,10, "Hit")
    hit_button.setSize(25)
    hit_button.unDraw()
    #Creates a hit button but undraws and deactivates it
    #for the time being

    stand_button = Button(blackjack, Point(70,10), 20,10, "Stand")
    stand_button.setSize(25)
    stand_button.unDraw()
    #Creates a stand button but undraws and deactivates
    #it for the time being

    quit_button = Button(blackjack, Point(95,5),7,5, "Quit")
    quit_button.unDraw()
    #Creates a quit button but undraws and deactivates it
    #for the time being

    introduction = Button(blackjack, Point(50,50), 95,20, \
    "Welcome to the Blackjack Game!\nEnter your bet and press continue.")
    introduction.setSize(25)
    #Prints the introduction of the game and asks the user
    #to place their bet and press continue

    global continue_button
    continue_button = Button(blackjack, Point(50, 15), 25, 10, "Continue")
    continue_button.setSize(25)
    #Draws the continue button which the user must press

    global bank
    bank = Bank(blackjack, 90, 90, "money.txt", "highscores.txt")
    #Initialises the bank of the player for this game

    betEntry = Entry(Point(50, 30), 20)
    betEntry.draw(blackjack)
    #Draws the entry box where the user puts in his bet

    hit_or_stand = blackjack.getMouse()

    while not continue_button.isClicked(hit_or_stand):
        hit_or_stand = blackjack.getMouse()
    #Used to get a mouseclick and keep getting a mouseclick
    #until the user clicks the continue button

    bet = int(betEntry.getText())
    #Gets the bet amount from the textbox

    while bet > bank.currentAmount() or bet <= 0:
    #Checks if the user is betting more than they have
    #or lesser than 0

        wrong_bet = Button(blackjack, Point(50,70), 70,15, \
        "Please enter a bet more than 0\nupto the amount you have in bank")
        wrong_bet.setSize(20)
        #If they are, tells them to only bet as much
        #as they have and greater than 0

        hit_or_stand = blackjack.getMouse()
        while not continue_button.isClicked(hit_or_stand):
            hit_or_stand = blackjack.getMouse()
        #Gets a mouseclick and keeps getting a mousclick
        #until the user clicks continue

        bet = int(betEntry.getText())
        #Gets the text from the entry box
        
        wrong_bet.unDraw()
        #Undraws the wrong bet prompt

    betEntry.undraw()
    #Undraws the entry box for the bet

    introduction.unDraw()
    #Undraws the introduction of the game

    game_1 = Blackjack()
    d_hand, p_hand = game_1.initDeal(blackjack, 20, 70, 20, 30)
    #Initialises the game of blackjack and deals out the initial
    #cards for each player  

    if game_1.evaluateHand(d_hand) == 21:
        if not game_1.evaluateHand(p_hand) == 21:
    #If the dealer has blackjack and the player does not,
    #this statement is True

            dealer_total = game_1.dealerPlays(blackjack, 20,70)
            #Evaluates dealer total and reveals his cards to the player

            dealer_blackjack = Button(blackjack, Point(70,50), 60, 10, \
            "Dealer has blackjack!")
            dealer_blackjack.setSize(25)
            #Informs the user that the dealer has made blackjack and
            #that player has lost

            continue_button.unDraw()
            #Undraws the continue button

            quit_button.Draw()
            #Now enables the quit button now that game has ended

            bank.betLost(int(bet * 1.5))
            #Subtracts the amount that the user has lost from his
            #bank which is 1.5 times their bet

            if bank.isBroke():
            #Checks if the user is broke
                
                broke_button = Button(blackjack, Point(70,30), 50,10, \
                "You're Broke\n Please click quit to exit the game")
                broke_button.setSize(15)
                #If the user is broke, he is prompted that he is broke
                #and is asked to quit the game
                
                hit_or_stand = blackjack.getMouse()
                #Waits for a mouselick

                while not quit_button.isClicked(hit_or_stand):

                    hit_or_stand = blackjack.getMouse()
                    #Waits for a mouselick

                endGame()
                #Ends the game

            else:

                replay = Button(blackjack, Point(70,30), 30, 10, \
                "Play again")
                replay.setSize(20)
                hit_or_stand = blackjack.getMouse()
                #If the user is not broke, asks the user if
                #they want to play again

                while (not replay.isClicked(hit_or_stand)) and (not quit_button.isClicked(hit_or_stand)):
                #Keeps getting a mouselick until the user clicks
                #one of the buttons

                    hit_or_stand = blackjack.getMouse()

                if replay.isClicked(hit_or_stand):
                    blackjack.close()
                    main()
                #If the user wishes to play again, the
                #main() function is recalled

                elif quit_button.isClicked(hit_or_stand):

                    endGame()
                    #Ends the game
        

    elif game_1.evaluateHand(p_hand) == 21:
        if not game_1.evaluateHand(d_hand) == 21:
    #If the player has blackjack and the dealer does
    #not, this statement is True
            

            player_blackjack = Button(blackjack, Point(70,50), 60, 10, \
            "Player has blackjack!")
            player_blackjack.setSize(25)
            #Informs the user that they have gotten a blackjack
            #and that they have won

            continue_button.unDraw()
            #Undraws the continue button

            quit_button.Draw()
            #Enables the quit button as game has ended

            bank.betWon(int(bet * 1.5))
            #Adds the amount that the user has won to their bank,
            #which is 1.5 times their bet

            replay = Button(blackjack, Point(70,30), 30, 10, "Play again")
            replay.setSize(20)
            hit_or_stand = blackjack.getMouse()
            #Asks the user if they want to play again and
            #waits for a mouseclick

            while (not replay.isClicked(hit_or_stand)) and (not quit_button.isClicked(hit_or_stand)):
            #Keeps getting a mouselick until the user clicks one of the buttons

                hit_or_stand = blackjack.getMouse()

            if replay.isClicked(hit_or_stand):
                blackjack.close()
                main()
            #If the user wishes to play again, the main() function is recalled

            elif quit_button.isClicked(hit_or_stand):

                if bank.isHighscore(bank.currentAmount()):
                #Checks if the users score is a highscore before letting them quit
                
                    clearScreen()
                    highscore_button = Button(blackjack, Point(50,70), 70,20, \
                    "You got a new highscore!\nPlease enter your name and\nclick continue to save it")
                    highscore_button.setSize(25)
                    #If the score is a highscore, informs the user of that and asks
                    #for their name so it can be saved to the list of highscores

                    name_entry = Entry(Point(50,30), 30)
                    name_entry.draw(blackjack)
                    #Creates an entry box where the name is to be entered

                    continue_button.Draw()
                    continue_click = blackjack.getMouse()
                    #Creates the continue button which the user must
                    #click and checks for a mouseclick

                    while not continue_button.isClicked(continue_click):
                        continue_click = blackjack.getMouse()
                    #Keeps checking for a mouseclick until the user
                    #clicks the continue button

                    name = str(name_entry.getText())
                    #Saves the name that the user enters to a variable

                    name_entry.undraw()
                    #Undraws the entry box

                    bank.newHighscore(name, bank.currentAmount())
                    #Adds the new highscore to the list of highscores
                    #and saves it to the text file

                endGame()
                #Ends the game
                
                

    continue_button.unDraw()
    betEntry.undraw()
    #Undraws buttons which are not needed anymore

    hit_button.Draw()
    stand_button.Draw()
    #Draws the now required buttons

    xPos, yPos = 30 , 30
    #Initialises the positions for the first extra cards
    #which are dealt by hitting to be drawn onto

    hit_or_stand = blackjack.getMouse()
    #Used to get a mouseclick

    while not quit_button.isClicked(hit_or_stand):
    #Used to keep the game going until the
    #quit button is clicked

        if not hit_button.isClicked(hit_or_stand) and not stand_button.isClicked(hit_or_stand):
            hit_or_stand = blackjack.getMouse()
        #If no appropriate button is clicked, the program
        #will keep getting mouseclicks

        if hit_button.isClicked(hit_or_stand):
        #If the user clicks the hit button,
        #deals another card to the user
            
                game_1.hit(blackjack, xPos, yPos)
                xPos = xPos + 5
                #deals the card and updates the position
                #for the next card

                if game_1.evaluateHand(p_hand) > 21:
                #If the user total goes over 21 the player
                #busts and they lose

                    player_busts = Button(blackjack, Point(70,50), 50,10,
                    "Player has busted!")
                    player_busts.setSize(25)
                    #Informs the player that they have busted

                    hit_button.unDraw()
                    stand_button.unDraw()
                    #Undraws the playing buttons

                    quit_button.Draw()
                    #Now enables the quit button now that game has ended

                    bank.betLost(bet)
                    #Subtracts the amount that the user has lost from his bank

                    if bank.isBroke():
                    #Checks if the user is broke
                        
                        broke_button = Button(blackjack, Point(70,30), 50,10, \
                        "You're Broke\n Please click quit to exit the game")
                        broke_button.setSize(15)
                        #If the user is broke, he is prompted that he is
                        #broke and is asked to quit the game
                        
                        hit_or_stand = blackjack.getMouse()
                        #Waits for a mouselick


                    else:
                    
                        replay = Button(blackjack, Point(70,30), 30, 10, "Play again")
                        replay.setSize(20)
                        hit_or_stand = blackjack.getMouse()
                        #If the user is not broke, asks the user
                        #if they want to play again

                        if replay.isClicked(hit_or_stand):
                            blackjack.close()
                            main()
                        #If they want to play again, the main() function
                        #is called again with the updated bank value
                else:

                    hit_or_stand = blackjack.getMouse()
                    #If the user total is not above 21, simply
                    #waits for another click from the user

        if stand_button.isClicked(hit_or_stand):
        #If the stand button is clicked, evaluates
        #the result of the game

            player_total = game_1.evaluateHand(p_hand)
            dealer_total = game_1.dealerPlays(blackjack, 20,70)
            #Evaluates the player and dealer total after
            #making the dealer play his hand and show his cards

            if dealer_total > 21:
            #If the dealer goes over 21, he busts and he loses

                dealer_busts = Button(blackjack, Point(70,50), 50,10, \
                "Dealer has busted!")
                dealer_busts.setSize(25)
                #Tells the user that the dealer has busted and they have won

                hit_button.unDraw()
                stand_button.unDraw()
                #Undraws the playing buttons

                quit_button.Draw()
                #Enables the quit button as game has ended

                bank.betWon(bet)
                #Adds the amount that the player has won into their bank
                
                replay = Button(blackjack, Point(70,30), 30, 10, \
                "Play again")
                replay.setSize(20)
                hit_or_stand = blackjack.getMouse()
                #Asks the user if they want to play again and waits for a mouseclick

                if replay.isClicked(hit_or_stand):
                    blackjack.close()
                    main()
                #If the user chooses to play again, the main() function is recalled

            elif player_total > dealer_total:
                #If the player total is greater than the dealer total, the player win

                player_wins = Button(blackjack, Point(70,50), 50,10, \
                "Player wins!")
                player_wins.setSize(25)
                #Informs the player that they have won

                hit_button.unDraw()
                stand_button.unDraw()
                #Undraws the playing buttons

                quit_button.Draw()
                #Enables the quit button as game has ended

                bank.betWon(bet)
                #Adds the amount that the user has won to their bank
                
                replay = Button(blackjack, Point(70,30), 30, 10, \
                "Play again")
                replay.setSize(20)
                hit_or_stand = blackjack.getMouse()
                #Asks the user if they want to play again and waits for a mouseclick

                if replay.isClicked(hit_or_stand):
                    blackjack.close()
                    main()
                    #If the user wishes to play again, the main() function is recalled

            elif player_total < dealer_total:
            #If the player total is lesser than the dealer total, the player loses

                player_loses = Button(blackjack, Point(70,50), 50,10, \
                "Player loses!")
                player_loses.setSize(25)
                #Informs the player that they have lost

                hit_button.unDraw()
                stand_button.unDraw()
                #Undraws the playing buttons

                quit_button.Draw()
                #Draws the quit button now that the game has ended

                bank.betLost(bet)
                #Subtracts the amount that the user has lost from their bank
                
                if bank.isBroke():
                #Checks if user is broke
                    
                    broke_button = Button(blackjack, Point(70,30), 50,10, \
                    "You're Broke\n Please click quit to exit the game")
                    broke_button.setSize(15)
                    #If they are broke, informs them of that and asks
                    #them to quit the game
                    
                    hit_or_stand = blackjack.getMouse()
                    #Waits for a mouseclick


                else:
                #Otherwise, if they are not broke, asks the user
                #if they want to play again
                
                    replay = Button(blackjack, Point(70,30), 30, 10, \
                    "Play again")
                    replay.setSize(20)
                    hit_or_stand = blackjack.getMouse()
                    #Draws the play again button and waits
                    #for a mouseclick

                    if replay.isClicked(hit_or_stand):
                        blackjack.close()
                        main()
                    #If the play again button is clicked,
                    #then the main() functon is recalled

            elif dealer_total == player_total:
            #If the dealer total is equal to the player total,
            #no one wins and it is a standoff

                standoff = Button(blackjack, Point(70,50), 50,10, \
                "Standoff!")
                standoff.setSize(25)
                #informs the user that it is a standoff and no one wins

                hit_button.unDraw()
                stand_button.unDraw()
                #Undraws the playing buttons

                quit_button.Draw()
                #Draws the quit button now that the game has ended

                replay = Button(blackjack, Point(70,30), 30, 10, \
                "Play again")
                replay.setSize(20)
                hit_or_stand = blackjack.getMouse()
                #Asks the user if they want to play again and waits for a mouseclick

                if replay.isClicked(hit_or_stand):
                    blackjack.close()
                    main()
                #If the user wants to play again, the main() function is recalled

        
    checkHighscore()
    #Checks if user score is a highscore and if it is,
    #asks for their name, and updates it to the list

    endGame()
    #Ends the game

main()

            
        

        
