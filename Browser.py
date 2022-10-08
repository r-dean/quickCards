# card browser

from tkinter import *
from tkinter import ttk
import os
import csv

class browser(Frame):
    '''A class representing the frame which contains all the browser functionality'''
    def __init__(self, container):
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within'''
        self.container = container
        
        # use root frame to create subframe
        super().__init__(self.container)
                
                
        self.selected_deck  = 'All Decks'
        
        # create a dictionary of all cards
        self.card_dict = self.generateDict()
        
        # create a list of all cards to show in the selectFrame
        self.selected_list = []
        for card in self.card_dict:
            self.selected_list.append(card)
        
        self.card_list = tuple(self.selected_list)
        
        # frames
        # - back button
        back_button = Button(self, text='Back', fg='red', padx=20, command=self.backToMain)                

        # - tabs frame
        tab_frm = tabFrame(self, self.card_dict, self.deck_list)
        
        # - search frame
        # - card select frame
        self.select_frm = selectFrame(self, self.card_dict, self.selected_list)
        # - content frame
        self.content_frm = contentFrame(self, self.card_dict)
        
        
        # configure main layout        
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
      
        # grid frames to layout
        back_button.grid(column=0,row=0, sticky='nw')
        tab_frm.grid(column=0, row=1, sticky='nw')
        self.select_frm.grid(column=2,row=1, sticky = 'e')
        self.content_frm.grid(column=2,row=2, sticky ='e')
        
        # define actions to be preformed on closing
        self.container.protocol("WM_DELETE_WINDOW", self.onClosing)
        
        
    def onClosing(self):
        # save all changes before closing
        self.saveDict()
        self.container.destroy()
  
    def saveDict(self):
        for deck in self.deck_list:
            # build a list of all cards in the deck
            contained_list = []
            for card in self.card_dict:
                if self.card_dict[card][3] in deck:
                    contained_list.append(card)
                    
            # save all cards to the deck
            file = open('decks\\' + deck, 'w', encoding='utf8')
            fieldnames = ['card_id','front', 'back', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)            
            writer.writeheader()            
            for card in contained_list:
                card_id = card
                front = self.card_dict[card][0]
                back = self.card_dict[card][1]
                status = self.card_dict[card][2]            
                
                writer.writerow({'card_id': card_id, 'front': front, 'back': back, 'status': status})        
                
                    
        
    def generateDict(self):
        '''create a card dictornary of cards stored in all decks'''
        
        # get a list of all files in the decks directory
        path = '.\\decks'
        filelist = os.listdir(path) 
        
        # a list of all decks in the dictionary including '.csv' ending
        self.deck_list = []
        
        # find a list of all decks
        for filename in filelist:
            if filename.endswith('.csv'):
                self.deck_list.append(filename)        
        
        card_dict = {}        
        
        for filename in self.deck_list:        
            csvfile = open('decks\\' + filename, 'r', encoding='utf8')
            reader = csv.DictReader(csvfile)
            for row in reader:
                card_dict[row['card_id']] = [row['front'], row['back'], row['status'], filename[0:-4]]      
        return (card_dict)        

    def backToMain(self):
        '''Return to the mainpage'''
        self.saveDict()
        self.destroy()
        try:
            self.container.openMainpage()
        except:
            print('Error: container')
    
    def getSelected(self):
        '''Return the id of the currrently selected card'''
        card_id = self.select_frm.getSelected()
        return card_id
    
    def updateContent(self):
        '''destroy and refresh the content frame'''
        self.content_frm.destroy()
        self.content_frm = contentFrame(self, self.card_dict)
        self.content_frm.grid(column=2,row=2, sticky ='e')
    
    def updateSelectedList(self):
        '''update the cards to be included in the list to be displayed'''
        self.selected_list = list(self.card_list)
        
        remove_list = []
        
        if self.selected_deck != 'All Decks':
            for card in self.selected_list:
                
                if self.card_dict[card][3] != self.selected_deck:
                    remove_list.append(card)
                    
        for card in remove_list:
            self.selected_list.remove(card)
            
        self.updateSelected()
        
   
    def removeFromCardList(self, card):
        card_list = list(self.card_list)
        card_list.remove(card)
        self.card_list = tuple(card_list)
    
    def updateSelected(self):
        '''destroy and refresh the selected frame'''
        self.select_frm.destroy()
        self.select_frm = selectFrame(self, self.card_dict, self.selected_list)
        self.select_frm.grid(column=2,row=1, sticky = 'e')
        
    def updateSelectedDeck(self, deck):
        self.selected_deck = deck
        self.updateSelectedList()
        
class tabFrame(Frame):
    '''A class representing the frame which contains a list of all filters that can be applied to the cards'''

    
    def __init__(self, container, card_dict, deck_list):
        
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within
        :param card_dict: the dictionary object containing all the information associated with each card'''
        
        self.card_dict = card_dict
        self.container = container
    
        # use root frame to create subframe
        super().__init__(self.container)
        
        # content
        
        self.listbox = Listbox(self, font=("Arial",15), exportselection=False )
        
        self.listbox.insert(0, 'All Decks')
        
        i = 1
        
        for deck in deck_list:
            self.listbox.insert(i, deck[0:-4])
            i += 1
        
        self.listbox['height'] = i
        
        # create click event
        self.listbox.bind('<<ListboxSelect>>', self.selectionEvent)         
        
        # grid
        self.listbox.grid(row=0, column=0)
        
    def selectionEvent(self, event):
        '''Update the select frame whenever a new tab is chosen'''
        selection = self.listbox.curselection()
        deck = self.listbox.get(selection)
        self.container.updateSelectedDeck(deck)
        
class selectFrame(Frame):
    '''A class representing the frame which contains a list of all cards matching search filters that can be selected'''

    
    def __init__(self, container, card_dict, selected_list):
        
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within
        :param card_dict: the dictionary object containing all the information associated with each card
        :param selected_list: a list of all card ids for cards to be displayed'''
        
        self.container = container
        self.card_dict = card_dict
        self.selected_list = selected_list
        
    
        # use root frame to create subframe
        super().__init__(self.container)
        
        # create tree from all cards to be displayed
        i = 0
        
        columns = ('front', 'back', 'deck', 'id')
        display_columns = ('front', 'back', 'deck')
        
        tree = ttk.Treeview(self, columns=columns, displaycolumns=display_columns, show ='headings', height=100)
        
        # label the coloumns as they will be displayed
        tree.heading('front', text = 'Front')
        tree.heading('back', text= 'Back')
        tree.heading('deck', text= 'Deck')
        
        # create a list of all cards as tupples
        cards = []
        
        for card_id in selected_list:
            front = self.card_dict[card_id][0]
            back = self.card_dict[card_id][1]
            deck = self.card_dict[card_id][3]
            card = (front, back, deck, card_id)
            cards.append(card)
        
        # place cards in the tree
        for card in cards:
            tree.insert('', END, values=card)
        
        # configure coloumns
        tree.column(0, width = 200)
        
        self.tree = tree
        
        

            
        # create scrollbar 
        scrollbar = Scrollbar(self, command=self.tree.yview)
        
        self.tree['yscrollcommand'] = scrollbar.set
        
        # create click event
        self.tree.bind('<<TreeviewSelect>>', self.clicked)    
        
        # configure
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # grid
        tree.grid(row=0, column=0, sticky = 'nse')
        scrollbar.grid(row=0, column=1, sticky="nse")


    def clicked(self, event):
        '''Update the content of the content frame whenever a new item is selected'''
        self.container.updateContent()
        
    def getSelected(self):
        tree_select = self.tree.selection()
        tree_item = self.tree.item(tree_select, option='values')
        
        # if no item is selected return 0
        if tree_item == '':
            return 0
        # otherwise return the card id which is the fourth item in the item values
        else:
            card_id = tree_item[3]
            return card_id
        


    

class contentFrame(Frame):
    '''A class representing the frame which displays all the content of a given card'''
    def __init__(self, container, card_dict):
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within
        :param card_dict: the dictionary object containing all the information associated with each card
        '''
        self.container = container
        self.card_dict = card_dict
        
        # use root frame to create subframe
        super().__init__(self.container)
        
        # get contents from selection
        self.card_id = self.getSelected()
        
        if self.card_id == 0:
            test_label = Label(self, text='No card selected', font = ("Arial",20))
            test_label.pack()
            
        else:
            self.showCard()
            
        
        
    def getSelected(self):
        '''Return the id of the currrently selected card'''        
        card_id = self.container.getSelected()
        return card_id
    
    def showCard(self):
        front_text = self.card_dict[self.card_id][0]
        back_text = self.card_dict[self.card_id][1]
        
        textbox_width = 60
        
        
        self.front = Text(self, font=('Arial', 15), width=textbox_width, height = 3)
        self.front.insert(INSERT, front_text)
        self.back = Text(self, font=('Arial', 15), width=textbox_width, height = 3)
        self.back.insert(INSERT, back_text)
        
        
        action_frm = Frame(self)
        save_button = Button(action_frm, text='Save Changes', fg='green', font = ('Arial', 15), command = self.saveChanges)
        delete_button = Button(action_frm, text='Delete Card', fg='red', font = ('Arial', 15), command = self.deleteCard)
        
        delete_button.grid(row=0, column=0)
        save_button.grid(row=0, column=1)
        action_frm.grid(row=2, column=0, sticky ='e')
        self.front.grid(row=0, column=0)
        self.back.grid(row=1, column=0)
        
    def saveChanges(self):
        front_text = self.front.get(1.0, END)
        back_text = self.back.get(1.0, END)
        self.card_dict[self.card_id][0] = front_text
        self.card_dict[self.card_id][1] = back_text
        self.container.updateSelected()
        
    def deleteCard(self):
        del self.card_dict[self.card_id]
        self.container.removeFromCardList(self.card_id)
        self.container.updateSelectedList()
        self.container.updateContent()
    
if __name__ == '__main__':
                
        root = Tk(None, None, 'browser Test')
        root.geometry(f"{1200}x{500}")
        frame = browser(root)
        frame.pack(fill=BOTH)
        
        
        root.mainloop()