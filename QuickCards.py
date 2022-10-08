# import classes for subframes
from Flashcard import *
from Mainpage import *
from Creator import *
from Browser import *



class mainRoot(Tk):
    '''A class defining a Tk object with functionality for navigating between subframes'''
    def __init__(self):
        '''Create an instance of the object and open the mainpage'''
        
        # create base Tk object
        super().__init__(className='QuickCards')
        
        # set size
        self.geometry(f"{600}x{500}")
        
        # open the mainpage when starting the program
        self.openMainpage()
        
        # run the loop which handles the gui
        
        self.mainloop()
        
    
    def openDeck(self, deck):
        '''Create an instance of the mainFlashFrame class and place it within the root widget in order to display a specific deck
        :param deck: a string that represents the name of a specific deck to be opened'''
        
        print('opening', deck)
        
        # make the name of the deck match that of the csv file
        deck_file = deck + '.csv'
        
        # open a deck
        frame = mainFlashFrame(self, deck_file)
        frame.pack()
        

        
    def openMainpage(self):
        '''Create an instance of the mainFrame class in order to display the main page'''
        print('opening mainpage')        
        frame = mainFrame(self)
        frame.pack()        
        
    def openCardCreator(self,deck):
        '''Create an instance of the cardCreator class and place it within the root widget in order add cards to a specific deck
        :param deck: a string that represents the name of a specific deck to be edited'''        
        print('opening card creator')
        frame = cardCreator(self, deck)
        frame.pack()
        
    def openDeckCreator(self):
        '''Create an instance of the cardCreator class and place it within the root widget in order to create a new deck'''
        print('opening deck creator')
        frame = deckCreator(self)
        frame.pack()
    
    def openBrowser(self):
        '''Create an instance of the browser class and place in within the root widget'''
        print('opening card browser')
        frame = browser(self)
        frame.pack(fill=BOTH)
        


if __name__ == '__main__':
    mainRoot()
