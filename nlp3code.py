﻿#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:57:10 2018

@author: susandarvishi
"""

# make dictionary of POS where each value is a dictionary from words to freq.

class word:
    # frequencies we'll need a dictionary
    def __init__(self, name = None, freq = None):
        self.name = name
        self.freq = {}
class pos:
    def __init__(self, posname = None, followspos = None):
        self.posname = posname
        self.followspos = {}  
try:
    file_to_read = "smallertestfile.pos"
    with open(file_to_read, 'r') as f:
        #make class to take in word, freq, prob of word given the pos
        key = ""
        value = ""
        counts = []
        word_dict = {}
        freq = {}
        alllines = []
        allwords = []
        allpostags = []
        posdict = {}
        for line in f:
            lines = line.split()
            count = 0
            for each in lines:
                count +=1
                if count == 2:
                    allwords.append(lines[0])
                key = lines[0]
                value = lines[1]

                if key not in word_dict.keys() and count ==2:
                    temp ={lines[1]:1}
                    if lines[1].isalnum() == True:
                        wordobj = word(key, freq)
                        wordobj.freq.update(temp)                         
                        word_dict.update({key:wordobj})
                #print(word_dict.get(key))
                elif key in word_dict.keys() and lines[1] not in word_dict.get(key).freq and count == 2:
                    word_dict.get(key).freq[value] = 1
                    
                elif key in word_dict.keys() and lines[1] in word_dict.get(key).freq and count == 2:
                    word_dict.get(key).freq[value] +=1
                    
                if value not in allpostags and count ==2:
                    if value.isalnum() == True:
                        allpostags.append(value)
        counter = 0
        totalwords = []
        for i in range(len(allwords)):
            if allwords[i].isalnum() == True or len(str(allwords[i])) > 2:
                totalwords.append(allwords[i])
        for i in word_dict:
            wordobj = word_dict.get(i)
            print(wordobj.freq)

except FileNotFoundError:
    print('Error! File not found.')
else:
    print('Done reading file')
