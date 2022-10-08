# Anki test addon
# basic flashcard app

# module for GUI
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno


import random
import csv


class mainFlashFrame(Frame):
    '''A class representing the frame which contains all the flashcard functionality'''
    def __init__(self, container, name):
        '''Create the initial elements of the frame
        :param container: the parent root/frame that this frame will operate within
        :param name: a string representing the deck which needs to be opened'''
        
        # name of the deck for cards to be displayed from
        self.name = name
        self.container = container
        
        # create a dictionary of the cards in the deck from the info stored in the csv file
        self.card_dict = self.readCardDict()
        self.due = self.generateDueList()
        self.amount_due = len(self.due)
        
        
        # use root frame to create subframe
        super().__init__(self.container)
        
        
        # frames
        self.menu_frame = menuFrame(self)          
        self.filler_frm = Label(self, height=200, width=200)        
        
 
        # configure main layout        
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(2, weight=1)      
        
        
        # grid frames to layout
        self.menu_frame.grid(column=0,row=0)           
        self.filler_frm.grid(column=0,row=2)
        
        
        # create initial subframes
        if self.due == []:
            self.showEmptyState()
        else:   
            self.showHiddenState()
            
    def showHiddenState(self):
        '''Create and display the frames which will be seen in a cards hidden state'''
        self.state = 'hidden'        
        
        # variables
        self.card_id = self.due.pop()
        self.word = self.card_dict[self.card_id][0]
        self.answer = self.card_dict[self.card_id][1]
        
        # frames
        self.word_frm = wordFrame(self, self.word)
        self.show_frm = showAnswerFrame(self)           
        
        # grid frames to layout
        self.word_frm.grid(column=0,row=1)
        self.show_frm.grid(column=0,row=3)
        
    def showEmptyState(self):
        self.state = 'empty'
        
        self.empty_label = Label(self, text='Out of Cards', font=("Arial",20))
        
        self.empty_label.grid(column=0, row=2)
        
        
    def showAnswer(self):
        '''Create and display the frames which represents the cards defintion and the area for feedback'''
        self.state = 'shown'
        
        self.wipeHiddenState()
        
        self.def_frm = defFrame(self, self.answer)
        self.def_frm.grid(column=0,row=2)
        self.fb_frm = feedbackFrame(self)
        self.fb_frm.grid(column=0,row=3)        
        
        
    def nextCard(self):
        '''Get rid of the frames currently displayed and replace them with the frames for the next card, unless at end of due list'''
        
        self.wipeShownState()
        
        if self.due ==[]:
            self.showEmptyState()
        else:
            self.showHiddenState()
            print('New card loaded')

            
    def returnToMainpage(self):
        '''destroy frames related to displaying cards and open mainpage frame via container'''
        print ('returning to Mainpage')
        self.destroy()
        self.saveCardDict()
        try:
            self.container.openMainpage()
        except:
            print('Error: Container')
    
    def reshuffleCard(self):
        '''place current card at the back of the duelist'''
        self.due.insert(0, self.card_id)
        print('Card reshuffled')
        
    def updateCardStatus(self):
        '''flip the due status of a card'''
        
        if self.card_dict[self.card_id][2] == 'Due':
            self.card_dict[self.card_id][2] = 'Other'
            self.amount_due -= 1
        else:
            self.card_dict[self.card_id][2] = 'Due'
            self.amount_due += 1
            
        self.saveCardDict()        
        
    def readCardDict(self):
        '''create a card dictornary of cards from a csv file'''
        csvfile = open('decks\\' + self.name, 'r', encoding='utf8')
        reader = csv.DictReader(csvfile)
        card_dict = {}
        for row in reader:
            card_dict[row['card_id']] = [row['front'], row['back'], row['status']]      
        return (card_dict)
    
    def generateDueList(self):
        '''generate a list of cards that are due from the card dictionary'''
        due_list = []
        for card in self.card_dict:
            if self.card_dict[card][2] == 'Due':
                due_list.append(card)
        return due_list
    
    def saveCardDict(self):
        '''save the card dictionary to a csv file'''
        
        file = open('decks\\' + self.name, 'w', encoding='utf8')
        fieldnames = ['card_id','front', 'back', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)            
        writer.writeheader()
        
        for card in self.card_dict:
            card_id = card
            front = self.card_dict[card][0]
            back = self.card_dict[card][1]
            status = self.card_dict[card][2]
            
            writer.writerow({'card_id': card_id, 'front': front, 'back': back, 'status': status})        
        

        
        
    def resetCardDict(self):
        self.due = []        
        self.amount_due = 0
        for card in self.card_dict:
            self.card_dict[card][2] = 'Due'
            self.due.append(card)
            self.amount_due += 1
        
        self.saveCardDict()
        self.resetSelf()
        

    def resetSelf(self):
        if self.state == 'hidden':
            self.word_frm.destroy()
            self.wipeHiddenState()
        elif self.state == 'shown':
            self.wipeShownState()
        else:
            self.empty_label.destroy()
        
        if not self.due ==[]:
            self.showHiddenState()
        else:
            self.showEmptyState()
            
        
    def getAmountDue(self):
        return self.amount_due

    
    def wipeHiddenState(self):
        self.show_frm.destroy()
    def wipeShownState(self):
        self.word_frm.destroy()
        self.def_frm.destroy()
        self.fb_frm.destroy()
    def deleteCard(self):
        '''Delete the current card from the deck'''
        answer = askyesno(title='confirmation',message='Are you sure you want to delete this card?')
        
        if answer:
            self.card_dict.pop(self.card_id)
            self.saveCardDict()
            self.amount_due -= 1
            self.resetSelf()
    def shuffleQueue(self):
        if self.state != 'empty':
            print('shuffling cards')
            self.due.append(self.card_id)
            random.shuffle(self.due)        
            self.resetSelf()
        else:
            print('no cards to shuffle')



class wordFrame(Frame):
    '''A class representing the frame in which the target word will be displayed'''
    def __init__(self, container, word):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in
        :param word: the word to be displayed in the frame'''
        
        # use frame parent class to create subframe
        super().__init__(container)

        self.word = word
        self.label = Label(self, text=self.word, font=("Arial",20))
        self.label.grid(column=0,row=0)
    

class defFrame(Frame):
    '''A class representing the frame in which the defintion of a word will be displayed'''    
    def __init__(self, container, defintion):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in
        :param defintion: the defintion to be displayed in the frame'''  
        
        # use frame parent class to create subframe
        super().__init__(container)
        
        self.defintion = defintion
        
        self.label = Label(self, text=defintion, wraplength=500, font=("Arial",20))
        self.label.grid(column=0,row=0)       

class showAnswerFrame(Frame):
    '''A class representing the frame in which will react to user input in order to display the answer'''        
    def __init__(self, container):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in'''
        
        # use frame parent class to create subframe
        super().__init__(container)
        
        self.container = container
        remaining = self.container.getAmountDue()
        
        # elements
        self.remaing_label = Label(self, text = str(remaining), fg = 'green')
        self.button = Button(self, text ='Show Answer', padx= 20, command=self.showAnswer)
        
        # grid elements
        self.remaing_label.grid(column=0, row=0)
        self.button.grid(column=0, row=1)
        
        
        
    def showAnswer(self):
        '''Shows the defintion associated with the word by creating a frame containing the information, also replaces the answer frame with a feedback frame'''
        
        self.container.showAnswer()

class feedbackFrame(Frame):
    '''A class representing the frame in which will react to user feedback will be taken and reacted to'''          
    
    def __init__(self, container):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in'''
        
        self.container = container
        
        # use frame parent class to create subframe        
        super().__init__(container)
    
        
        #
        amount_due = self.container.getAmountDue()
        due_label = Label(self, fg= 'green', text =amount_due)
        due_label.grid(column=1, row=0)
        
        #
        correct_button = Button(self, fg = 'green', text ='Correct', padx= 20, command=self.correctAnswer)
        correct_button.grid(column=0, row=1)
        inbetween_space = Frame(self, width=30)
        inbetween_space.grid(column=1, row=1)
        incorrect_button = Button(self, fg = 'red', text ='Incorrect', padx= 20, command=self.incorrectAnswer)
        incorrect_button.grid(column=2, row=1)
        
        self.columnconfigure(1, weight = 1)        

        
    def correctAnswer(self):
        '''Change the current card's status from due and display the next card'''
        self.container.updateCardStatus()
        self.container.nextCard()
        
    def incorrectAnswer(self):
        '''Reshuffle the current card in the deck and display the next one'''
        self.container.reshuffleCard()
        self.container.nextCard()
        
class menuFrame(Frame):
    '''A class representing the frame in which the user can navigate back through other windows'''  
    
    def __init__(self, container):
        '''Generate the contents of the frame and place it within the parent frame
        :param container: the parent frame which this frame is to be placed in'''
        
        self.container = container
        
        # use frame parent class to create subframe        
        super().__init__(container)
        
        # elements
        back_button = Button(self, fg='red', text='Back', command=self.container.returnToMainpage, width =10)
        reset_button = Button(self, fg='orange', text='Reset Deck', width=13, command=self.container.resetCardDict)
        reshuffle_button = Button(self,fg='orange', text='Shuffle Deck', width=13, command=self.container.shuffleQueue)
        delete_button = Button(self, fg='red', text='Delete Card', command=self.container.deleteCard, width=10)

        # spaces
        space1= Label(self, width = 200)
        space2=Label(self, width= 200)
        space3= Label(self, width = 10)
        
        self.columnconfigure(1, weight=1)
        self.columnconfigure(4, weight=1)
        
        # grid elements to frame
        back_button.grid(column=0, row=0)
        space1.grid(column=1, row=0)
        reset_button.grid(column=2, row=0)
        reshuffle_button.grid(column=3,row=0)
        space2.grid(column=4, row=0)
        delete_button.grid(column=5,row=0)
        
        


if __name__ == '__main__':
        
        due_list = ['学校', '川', '手', '眼鏡']
        card_dict = {'学校':'School', '川':'River', '手':'Hand', '眼鏡':'Glasses'}       
        
        
        root = Tk(None, None, 'Flashcard Test')
        root.geometry(f"{600}x{500}")
        frame = mainFlashFrame(root, 'Test Deck.csv')
        frame.pack()
        root.mainloop()