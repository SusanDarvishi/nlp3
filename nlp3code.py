#!/usr/bin/env python3
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
    def __init__(self, numoccurrences = None, followspos = None):
        self.numoccurrences = numoccurrences
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
        posall = []
        for line in f:
            lines = line.split()
            count = 0
            for each in lines:
                count +=1
                if count == 2:
                    if lines[0] != '``':
                        allwords.append(lines[0])
                    if lines[1] != '``':
                        posall.append(lines[1])
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
        allwordswithstartend = allwords
        start = 'start'
        end = 'end'
        allwordswithstartend.insert(0, start)
        posall.insert(0, start)
        for i in range(len(allwordswithstartend)):
            if allwordswithstartend[i] == '.':
                allwordswithstartend[i] = 'end'
                allwordswithstartend.insert(i+1, start)
        length = len(allwordswithstartend)
        allwordswithstartend[length-1] = end
        for i in range(len(posall)):
            if posall[i] == '.':
                posall[i] = 'end'
                posall.insert(i+1, start)
        length2 = len(posall)
        posall[length-1] = end        

        print(posall)
        for i in range(len(posall)-1):
            prev = i
            current = i+1
            posprev = posall[prev]
            poscurrent = posall[current]
            if poscurrent not in posdict:
               # print('hey')
                postag = posall[prev]
                temp = {}
                follows = {postag:1}
                occurrences =1
                posobj = pos(occurrences, temp)
                posobj.followspos.update(follows)
                posdict.update({posall[current]:posobj})
                
            elif poscurrent in posdict and posprev not in posdict.get(poscurrent).followspos:
                posdict.get(poscurrent).numoccurrences +=1
                posdict.get(poscurrent).followspos[posprev] = 1
            elif poscurrent in posdict.keys() and posprev in posdict.get(poscurrent).followspos:
                posdict.get(poscurrent).numoccurrences +=1
                posdict.get(poscurrent).followspos[posprev] +=1
        for i in range(len(posall)-1):
            prev = i
            current = i+1
            posprev = posall[prev]
            poscurrent = posall[current]
            divide = float(posdict.get(poscurrent).numoccurrences)
            value = float(posdict.get(poscurrent).followspos.get(posprev))
            probability = value/divide
            posdict.get(poscurrent).followspos[posprev] = probability
        for i in posdict:
            print(i)
            print(posdict.get(i).numoccurrences)
            print(posdict.get(i).followspos)
        for i in range(len(allwords)):
            if allwords[i].isalnum() == True or len(str(allwords[i])) > 2:
                totalwords.append(allwords[i])
        for i in word_dict:
            wordobj = word_dict.get(i)
           

except FileNotFoundError:
    print('Error! File not found.')
else:
    print('Done reading file')
    
#    prob that current state is noun give previous state is verb
    
    
