# module for GUI
from tkinter import *
from tkinter import ttk
import csv, string, random

class cardCreator(Frame):
    
    '''A class representing the frame which contains all card creation functionality'''
    def __init__(self, container, name):
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within
        :param name: a string representing the deck which needs to be edited'''
        
        self.container = container
        self.name = name
        
        # use root frame to create subframe
        super().__init__(self.container)
                
        
        # - text boxes and labels
        front_label = Label(self, text='Front')
        self.front_box = Text(self, width=30, height=3)
        back_label = Label(self, text='Back')
        self.back_box = Text(self, width=30, height=3)
        blank_space = Label(self, height=200)
        
        # - action buttons
        action_frame = actionFrame(self)
        
        # configure main layout      
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(4, weight = 1)
    
        # grid frames to layout
        front_label.grid(column=0,row=0)
        self.front_box.grid(column=0,row=1)
        back_label.grid(column=0,row=2)
        self.back_box.grid(column=0,row=3)
        blank_space.grid(column=0,row=4)
        
       
        action_frame.grid(column=0,row=5)

        
    def getText(self):
        '''return a list containing a string for each textbox'''
        
        front_text = self.front_box.get('1.0', 'end')
        back_text = self.back_box.get('1.0','end')
        self.front_box.delete('1.0', 'end')
        self.back_box.delete('1.0', 'end')
        
        front_text = front_text.strip()
        back_text = back_text.strip()
 
        return [front_text, back_text]
    
    def writeCard(self):
        '''Append an entry for the created card to a csv file'''
        filename = self.name + '.csv'
        
        file = open('decks\\' + filename, 'a', encoding='utf8')
        fieldnames = ['card_id','front', 'back', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)        
        
        letters = string.ascii_letters

        card_id = (''.join(random.choice(letters) for i in range (10)))
        
        front, back = self.getText()
        
        writer.writerow({'card_id': card_id, 'front': front, 'back': back, 'status': 'Due'})
        
        file.close()
        
    def backToMain(self):
        '''Return to the mainpage'''
        self.destroy()
        try:
            self.container.openMainpage()
        except:
            print('Error: container')
            
            
class deckCreator(Frame):
    '''A class representing a frame with all deck creation functionality'''
    def __init__(self, container):
        '''Create the frame and its inital subframes
        :param container: the frame/root that the frame will be displayed within'''
        print(type(self))
        
        self.container = container
    
        # use root frame to create subframe
        super().__init__(self.container)
        
        # - text boxes and labels
        name_label = Label(self, text='Deck Name')
        self.name_box = Text(self, width=30, height=3)
        blank_space = Label(self, height=200)  
        
        # - action buttons
        action_frame = actionFrame(self)
        
        # configure main layout        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight = 1)
        
        # grid to layout'
        name_label.grid(column=0,row=0)
        self.name_box.grid(column=0,row=1)
        blank_space.grid(column=0,row=2)
        action_frame.grid(column=0,row=3)
        
    def createDeck(self):
        '''Create a csv deck file for the name provided'''
        name = self.name_box.get('1.0', 'end')
        self.name_box.delete('1.0', 'end')
        name = name.strip()
        
        filename = name + '.csv'
        
        file = open('decks\\' + filename, 'w', encoding='utf8')
        fieldnames = ['card_id','front', 'back', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)    
        
        writer.writeheader()
        
        file.close()
        
        
    
    def backToMain(self):
        '''Return to the mainpage'''
        self.destroy()
        try:
            self.container.openMainpage()
        except:
            print('Error: container')
    
    
class actionFrame(Frame):
    '''A class representing the frame containing the action buttons'''
    def __init__(self, container):
        '''Create the frame and its elements
        :param container: the frame/root that the frame will be displayed within'''    

        self.container = container
    
        # use root frame to create subframe
        super().__init__(self.container)
        
        # elements 
        back_button = Button(self, text='Back', fg='red', padx=20, command=self.back)          
        blankspace = Label(self, width=5)
        add_button = Button(self, text='Add', fg='green', padx=20, command=self.add)
        
        # configure layout
        self.columnconfigure(1, weight=1)
        
        # grid elements
        back_button.grid(column=0, row=0)
        blankspace.grid(column=1, row=0)
        add_button.grid(column=2, row=0)
        
        
    def back(self):
        '''Return back to the mainpage'''
        self.container.backToMain()
        
    def add(self):
        '''Perform the relevant add functionality for the container'''
        
        if type(self.container) == deckCreator:
            self.container.createDeck()
            
        elif type(self.container) == cardCreator:
            self.container.writeCard()
            
if __name__ == '__main__':
        
        root = Tk(None, None, 'cardCreator Test')
        root.geometry(f"{600}x{500}")
        frame = cardCreator(root, 'Test Deck')
        frame.pack()
        
        root2= Tk(None, None, 'deckCreator Test')
        root2.geometry(f"{600}x{500}")
        frame = deckCreator(root2)
        frame.pack()        
        
        
        root.mainloop()