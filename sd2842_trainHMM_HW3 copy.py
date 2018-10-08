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
    def updatePreviousPOS(self,key, value):
        self.previousPOS[key] = value
posdict = {}
word_dict = {}
allwords = []
posall = []
try:
    file_to_read = "smallertestfile.pos"
    with open(file_to_read, 'r') as f:
        #make class to take in word, freq, prob of word given the pos
        key = ""
        value = ""
        counts = []
       # word_dict = {}
        freq = {}
        alllines = []
        #allwords = []
        allpostags = []
       # posdict = {}
      #  posall = []
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
        
       # print(posall)
       # print(posall)
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
       # for i in posdict:
          #  print(i)
           # print(posdict.get(i).numoccurrences)
            #print(posdict.get(i).followspos)
        for i in range(len(allwords)):
            if allwords[i].isalnum() == True or len(str(allwords[i])) > 2:
                totalwords.append(allwords[i])
        
        
# =============================================================================
#         for i in word_dict:
#             print(i)
#             wordobj = word_dict.get(i)
#             print(wordobj.freq)
# =============================================================================
        

except FileNotFoundError:
    print('Error! File not found.')
else:
    print('Done reading file')
    
# =============================================================================
# for i in posdict:
#     print(i)
#     print(posdict.get(i).numoccurrences)
#     print(posdict.get(i).followspos)
#     
# for i in word_dict:
#     print(i)
#     wordobj = word_dict.get(i)
#     print(wordobj.freq)
# =============================================================================
#print(allwords)
totalwords = []
for i in allwords:
    if i != 'start' and i != 'end':
        totalwords.append(i)

#print(totalwords)
    
# =============================================================================
# 
# 
# class posObject:
#     numOccurances = -1
#     previousPOS = {}
# 
#     def __init__(self, numOccurances, previousPOS):
#         self.numOccurances = numOccurances
#         self.previousPOS = previousPOS
# 
#     def updatePreviousPOS(self,key, value):
#         self.previousPOS[key] = value
# =============================================================================

#the following dictionaries and arrays are expected output from parsing algorithm
wordDict = word_dict
# =============================================================================
# print('printing')
# for i in wordDict:
#     print(i)
#     print(wordDict.get('In').freq.get('IN'))
# =============================================================================
 
 

posDict = posdict

# =============================================================================
# =============================================================================
# for i in posDict:
#     print(i)
#     print(posDict.get(i).numoccurrences)
#     print(posDict.get(i).followspos)
# =============================================================================
 
# =============================================================================
totalWords = totalwords

#print(totalWords)



totalPOS = []
for i in posDict:
    totalPOS.append(i)

#print(totalPOS)



#----------------------------------------------------------------------------------------------------------------

numUniqueWords = len(totalWords)
numUniquePOS = len(totalPOS)


#this array will hold the proabilities and is nxm where n is num unique words and m is num pos
A = {}

for pos in totalPOS:
	A[pos] = [None for x in range(numUniqueWords+2)]
#this array will be the backtracking trace, it will be the same size as A and will hold in each position the location of the position that should precede it
B = {}

for pos in totalPOS:
    B[pos] = [None for x in range(numUniqueWords+2)]


#want to set the first column probabilities to 0 except the probability for start because there is a 100% chance that start is at the beginning
#of the sentence and a 0% chance that anything besides start begins a sentence
for pos in totalPOS:
	A[pos][0] = 0

A["start"][0] = 1

#embed()

#this next set of for loops will fill out both array A and array B
#array A will hold the probabilities for each circumstance, and B will hold the backtrack path

lastGenerated = {"start":1}
tempLastGenerated = {}




#begin by looking at each word
for word in totalWords:
	#print(word)
	#look at all the pos that can preceed that word
    for prevpos in lastGenerated.keys():
		#print (prevpos)
		#now we want to try to find the pos that can apply to word that can also follow prevpos
		#so we start by going over all the pos that apply to the word
        for pos in wordDict.get(word).freq.keys():
		#	print (pos)
            # THIS LINE NEEDS TO BE FIXED
			#and then we confirm that it is a pos that can follow the previous pos
            if prevpos in posDict.get(pos).followspos.keys():
				#once we've confirmed, we can begin calculations
				#first calculate the probability that prevpos preceeds pos -- this is equal to the probability that this pos follows
				#prevpos times the probability calculated for prevPos
                probWordIsPOS = float(wordDict.get(word).freq.get(pos))/posDict.get(pos).numoccurrences
                probPrevposPreceeds = posDict.get(pos).followspos.get(prevpos) * lastGenerated.get(prevpos) * probWordIsPOS
				#print (probPrevposPreceeds)
				#print (posDict.get(pos).followspos.get(prevpos))
				#print (probWordIsPOS)
				#add to dictionary in wider scope
                if pos in tempLastGenerated.keys():
					#if that pos is already in that dictionary, we want to take the maximum
                    tempLastGenerated[pos] = max(probPrevposPreceeds, tempLastGenerated.get(pos))
                else:
					#if not, just add it
                    tempLastGenerated[pos] = probPrevposPreceeds
			#else we will not calculate probability because there is no chance that the pos can follow the prevpos

    lastGenerated = tempLastGenerated
    tempLastGenerated = {}
	
#	print (lastGenerated)

	#at the end of these for loops we have the probability that each pos applies to each word
	#now we need to add those probabilities to the final array A
    for key in lastGenerated:
		#for each pos that we've calculated we need to add that probability to array A at position totalWords.index(word)
        A[key][totalWords.index(word)+1] = lastGenerated.get(key)

 #   print (A)

# read in new file
# dictionary of all words
#dictofallwords = {{'In':'IN'}, {'an':'DT'}, {'Oct.':'NNP'}, {'19':'CD'}, {'review':'NN'}, {'of': 'IN'}, {'was':'VBD'}, {'mistakenly':'RB'}, {'attributed':'VBN'}, {'to':'TO'}, {'Christina': 'NNP'}, {'Haag':'NNP'}}                                    }

try:
    dictofallwords = {'In':'IN', 'an':'DT', 'Oct.':'NNP', '19':'CD', 'review':'NN', 'of': 'IN', 'was':'VBD', 'mistakenly':'RB', 'attributed':'VBN', 'to':'TO', 'Christina': 'NNP', 'Haag':'NNP'}                                   
   # print(dictofallwords.keys())
    newwords= []
    file_to_read = "smallertestfile.words"
    with open(file_to_read, 'r+') as f:
        for word in f:
           # print(word)
            if word != None:
                newwords.append(word)
        
        for i in range(len(newwords)):
            newwords[i] = newwords[i].strip('\n')
           # print(newwords)
        answers = []
        for i in newwords:
            if i in dictofallwords.keys():
                answers.append(dictofallwords.get(i))
            
        
except FileNotFoundError:
    print('Error! File not found.')
else:
    print('Done reading file')
# dictionary where we check if word is in the dict, return pos

