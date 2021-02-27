#  -*- coding: utf-8 -*-
'''
P7
Derek Nguyen
Created: 2019-03-26
Modified: 2019-03-26
Due: 2019-03-27
'''

# %% codecell

import string
import random
import numpy as np
import pandas as pd


# Path to .csv file to read
# csvFile = 'C:\Users\derek\Box Sync\SP20\CBE 5790\HW\English_words.csv'

# Upload the data set into a Pandas Data Frame
englishWords = pd.read_csv(r'~/English_words.csv')

# Convert the columns to tuples
ranks = tuple(englishWords.loc[:,'Rank'])
words = tuple(englishWords.loc[:,'Word'])
pos = tuple(englishWords.loc[:,'Part of speech'])
freqs = tuple(englishWords.loc[:,'Frequency'])
disp = tuple(englishWords.loc[:,'Dispersion'])

# String of allowed characters
char = string.ascii_letters + ' '

# Calculate and store lengths of words
lengths = [] # creates an empty list
for word in words:
    lengths.append(len(word))

def seqscore(inseq = None):
    '''
    Scoring function to assign a score to a string based on its resemblance to the english language.
    Parameters:
    inseq, a string
    '''

    score = 0

    seq = inseq.split(' ') # splits the string into a list of words called seq

    for ii, word in enumerate(words):
        for part in seq:
            if word in part: # gives a point for a phrase that contains a word from the word list
                score += 1

            if part == word: # gives points for each word matching a word from the word list based the rarity of the word
                score += ranks[ii] # the more rare the word, the greater the points


    return score

def evolver(parent = 'Beware of ManBearPig', nGen = 1000, nChildren = 20, mutationProbs = (0.01, 0.002, 0.002), printGens = False):
    '''
    evolution function to mutate a string based on mutation probilities through a specified number of generations and children
    Parameters:
    parent, a string
    nGen, an integer
    nChildren, an integer
    mutationProbs, a tuple of 3 probabilities
    printGens, a boolean
    '''
    if type(parent) is not str:
        raise TypeError('Parent must be a string')
    if type(nGen) is not int:
        raise TypeError('nGen must be an integer')
    if type(nChildren) is not int:
        raise TypeError('nChildren must be an integer')
    if type(mutationProbs) is not tuple:
        raise TypeError('mutationProbs must be a tuple')
    if type(printGens) is not bool:
        raise TypeError('nGen must be an integer')

    subProb, delProb, insProb = mutationProbs

    for generation in range(nGen): # iterates through each generation
        score = None

        for ii in range(nChildren): # iterates through each child
            child = '' # creates empty child

            for jj in parent: # iterates through each character of the parent and mutates the character based on the mutationProbs

                # Allow for one possible mtation per site
                mutation = random.choice(('sub', 'del', 'ins'))
                if mutation == 'sub' and np.random.binomial(1,subProb) == 1:
                    jj = random.choice(char)
                elif mutation == 'del' and np.random.binomial(1,delProb) == 1:
                    jj = ''
                elif mutation == 'ins' and np.random.binomial(1,insProb) == 1:
                    side = random.choice(('before', 'after'))
                    if side == 'before':
                        jj = random.choice(char) + jj
                    else:
                        jj = jj + random.choice(char)

                child = child + jj

            tem = seqscore(child) # scores the child utilizing seqscore

            if score is None or tem > score: # if the score is greater than the previous score set as new the new score
                score = tem
                next_parent = child


        parent = next_parent # reassigns new parent based on the highest scoring child
        if printGens:
            print('Gen ', generation, '\tScore = ', score, '\t', parent)

    print(parent) # prints the highest scoring parent

evolver()
