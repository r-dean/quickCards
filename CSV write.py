# csv dict creator

import csv
import random
import string

word_pairs = [('学校', 'School'), ('川', 'River'), ('手', 'Hand'), ('眼鏡', 'Glasses')]

file = open('.\\decks\\Test Deck.csv', 'w', encoding='utf8')

fieldnames = ['card_id','front', 'back', 'status']
writer = csv.DictWriter(file, fieldnames=fieldnames)

letters = string.ascii_letters

writer.writeheader()


for i in range (10):
    card_id = (''.join(random.choice(letters) for i in range (10)))
    front = i
    back = 'Sample Text'
    
    writer.writerow({'card_id': card_id, 'front': front, 'back': back, 'status': 'Due'})



file.close()