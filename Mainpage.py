# Class with functionality controlling the mainpage of the app

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno

import os
from functools import partial


class mainFrame(Frame):
    '''A class representing the frame which contains all the mainpage functionality'''
    def __init__(self, container):
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within'''
        self.container = container
        
        # use root frame to create subframe
        super().__init__(self.container)
        
        # create initial subframes        
        
        # frames
        deck_label = Label(self, text='Decks:', font=("Arial",15))
        self.decks_frm = decksFrame(self)
        self.action_frm = actionFrame(self)
        self.filler_frm = Label(self, height=200)
        # - top menu
        
    
        
        # configure main layout        
        self.rowconfigure(2,weight=1)
        
      
        # grid frames to layout
        deck_label.grid(column=0,row=0)
        self.decks_frm.grid(column=0,row=1)
        self.filler_frm.grid(column=0,row=2)
        self.action_frm.grid(column=0,row=3)
        
        # define actions to be taken on closing
        self.container.protocol('WM_DELETE_WINDOW', self.onClosing)
        
    def onClosing(self):
        self.container.destroy()
        
    def openDeck(self, deck):
        '''Close this frame and open a specific deck frame
        :param deck: the name of the deck to be opened'''
        
        
        try:
            self.container.openDeck(deck)
        except:
            print('could not open deck')
        else:
            self.destroy()
            

        
    def createDeck(self):
        print('mainPageFrame level call to card creator')
        
        
        try:
            self.container.openDeckCreator()
        except:
            print('Error: Could not open card creator')
        else:
            self.destroy()

            
    def addCard(self, deck):
        '''Close this frame and open a card creator frame via container
        :param deck: the name of the deck to be opened'''
        
        
        print('mainpageMainFrame level call to card creator')
        try:
            self.container.openCardCreator(deck)
        except:
            print('Error: container')
        else:
            self.destroy()
            
    def refreshDecksFrame(self):
        print('resfreshing decks frame')
        self.decks_frm.destroy()
        self.decks_frm = decksFrame(self)
        self.decks_frm.grid(column=0,row=1)

    def openBrowser(self):
        print('mainPage level call to cardBrowser')
        try:
            self.container.openBrowser()
        except:
            print('could not open browser')
        else:
            self.destroy()
                

class actionFrame(Frame):
    '''A class representing the frame in which different actions can be preformed from the mainpage'''
    def __init__(self, container):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in'''
        
        self.container = container
        
        # use frame parent class to create subframe
        super().__init__(self.container)
        
        # elements
        browse_button = Button(self, text='Card Browser', command=self.openBrowser)
        create_deck_button = Button(self, text='Create Deck', command=self.createDeck)
        
        # grid elements to frame
        browse_button.grid(column=0, row=0)
        create_deck_button.grid(column=1, row=0)
                                
        
    def createDeck(self):
        print('actionFrame level call to deckCreator')
        self.container.createDeck()
        
    def openBrowser(self):
        print('actionFrame level call to cardBrowser')
        self.container.openBrowser()


class decksFrame(Frame):
    '''A class representing the frame in which the created decks will be displayed and be chosen from'''
    def __init__(self, container):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in'''
        
        self.container = container
        
        # use frame parent class to create subframe
        super().__init__(self.container)
        
        self.decks = self.getDecks()
        if self.decks == []:
            print('no decks found')
            empty_label = Label(self,text='nothing to see here', font=('Arial',11))
            empty_label.grid(column=0,row=0)            
        else:
            self.displayDecks()
                
                
    def openDeck(self, deck):
        '''Close this frame and open a specific deck frame via a method in the container class
        :param deck: the name of the deck to be opened'''        
        
        self.container.openDeck(deck)
        
    def addCard(self, deck):
        '''Close this frame and open a card creator frame via container
        :param deck: the name of the deck to be opened'''
        
        print('decksFrame level card creator call')
        self.container.addCard(deck)        
    
    def deleteDeck(self, deck):
        '''Delete the deck and update the screen'''
        
        answer = askyesno(title='confirmation', message='Are you sure you want to delete this deck?')
        
        
        if answer:
            print('deleting', deck)
            filename = '.\\decks\\' + deck + '.csv'
            
            
            if os.path.exists(filename):
                
                os.remove(filename)
            else:
                print(filename, "does not exist")
            
            
            self.container.refreshDecksFrame()
        
        
    def displayDecks(self):
        '''Display all the decks in the deck frame'''
        
        print('displaying decks')
        
        i=0
        for deck in self.decks:
            # use partial function to allow argument to be passed to function openDeck function
            deck_selector = Button(self, anchor='w', fg = 'black', text = deck, width = 20, command=partial(self.openDeck, deck)) 
            add_card = Button(self, text = 'Add Cards', fg='green', command=partial(self.addCard, deck))
            delete_deck = Button(self, text = 'Delete', fg='red', command=partial(self.deleteDeck, deck))
            deck_selector.grid(column=0, row=i)
            add_card.grid(column=1, row=i)
            delete_deck.grid(column=2, row=i)
            i+=1        
        
    
        
    def getDecks(self):
        '''Look in folder and find all deck files'''
        
        print('looking for decks')
        
        path = '.\\decks'
        
        filelist = os.listdir(path) 
        
        deck_list =[]
        
        for filename in filelist:
            if filename.endswith('.csv'):
                filename = filename[:-4]
                deck_list.append(filename)
                
        deck_list.sort()
        return deck_list
        
        
        
        
if __name__ == '__main__':
    root = Tk(None, None, 'Mainpage Test')
    root.geometry(f"{600}x{500}")
    
    frame = mainFrame(root)
    
    frame.pack()
    root.mainloop()