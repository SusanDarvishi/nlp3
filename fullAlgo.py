from IPython import embed

class posObject:
    numOccurances = -1
    previousPOS = {}

    def __init__(self, numOccurances, previousPOS):
        self.numOccurances = numOccurances
        self.previousPOS = previousPOS

    def updatePreviousPOS(key, value):
        self.previousPOS[key] = value

posDict = {}
wordDict = {}
totalWords = []
totalPOS = []

filepath = 'WSJ_24.pos'  
with open(filepath) as fp:

    #begin by saying that the first pos is start
    prevPOS = "start"
    #add it to the pos dictionary with no pos that can preceed it
    posDict["start"] = posObject(1, None)
    totalPOS.append("start")

    #also add end so that it's there for when we run into it but leave occurrances at 0
    posDict["end"] = posObject(0, {})
    totalPOS.append("end")

    for cnt, line in enumerate(fp):
        #print("Line {}: {}".format(cnt, line))
        splitLine = line.split()
        #print(splitLine)

        if len(splitLine) == 2:
            if (not splitLine[0] == ".") and (not splitLine[0] == ",") and (not splitLine[0] == "``"):
                word = splitLine[0]
                pos = splitLine[1]
                #print word, pos
                #if we've never seen the word before
                if word not in wordDict.keys():
                    #add it to the word dictionary with the part of speech that we see it as
                    wordDict[word] = {pos:1}
                    #add it to the list of total words
                    totalWords.append(word)
                #if we have seen the word before
                elif word in wordDict.keys():
                    #check if we've already seen it as this part of speech
                    if pos in wordDict.get(word).keys():
                        #if we have, increment the number of occurrences on that pos
                        oldNumOccurrences = wordDict.get(word).get(pos)
                        wordDict.get(word)[pos] = oldNumOccurrences + 1
                    elif pos not in wordDict.get(word).keys():
                        #if not, add the new pos
                        wordDict.get(word)[pos] = 1
                    else:
                        print("error: for some reason not hitting either if statement when parsing a word's pos")
                else:
                    print("error: for some reason not hitting either if statement when parsing a word")

                #if we've never seen any word as this pos before (not just this word but any word)
                if pos not in posDict.keys():
                    #add it to the pos dictionary
                    posDict[pos] = posObject(1, {prevPOS: 1})
                    #add it to the list of total pos
                    totalPOS.append(pos)
                #if we have seen at least one word as this pos before (ie is already in posDict)
                elif pos in posDict.keys():
                    posDict.get(pos).numOccurances = posDict.get(pos).numOccurances + 1
                    #if this is the first time this pos is following prevPOS
                    if prevPOS not in posDict.get(pos).previousPOS.keys():
                        #add prevPOS to the previousPOS dictionary with an occurance of 1
                        posDict.get(pos).previousPOS[prevPOS] = 1
                    #if this is not the first time this pos is following prevPOS
                    elif prevPOS in posDict.get(pos).previousPOS.keys():
                        oldNumOccurrences = posDict.get(pos).previousPOS.get(prevPOS)
                        posDict.get(pos).previousPOS[prevPOS] = oldNumOccurrences + 1
                    else:
                        print("error: for some reason not hitting either if statement when parsing pos's previouspos")
                else:
                    print("error: for some reason not hitting either if statement when parsing a pos")

        else:
            #conditionwhen we're looking at a newline character aka a new sentence
            #so we need to first increment number of times that end appears and record the pos that preceeds it
            posDict.get("end").numOccurances = posDict.get("end").numOccurances + 1
            if prevPOS not in posDict.get("end").previousPOS.keys():
                #add prevPOS to the previousPOS dictionary with an occurance of 1
                posDict.get("end").previousPOS[prevPOS] = 1
            #if this is not the first time this pos is following prevPOS
            elif prevPOS in posDict.get("end").previousPOS.keys():
                oldNumOccurrences = posDict.get("end").previousPOS.get(prevPOS)
                posDict.get("end").previousPOS[prevPOS] = oldNumOccurrences + 1
            else:
                print("error: for some reason not hitting either if statement when parsing pos's previouspos")

        #set the prevPOS for the next word that we encounter
        prevPOS = pos

    print

    print ("WORDDICT ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print (wordDict)

    print

    print("POSDICT ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for key in posDict.keys():
        print(key, posDict.get(key).numOccurances, posDict.get(key).previousPOS)


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
    print "--------------------------------------------------------------------------"
    print word
    #look at all the pos that can preceed that word
    for prevpos in lastGenerated.keys():
        print prevpos
        #now we want to try to find the pos that can apply to word that can also follow prevpos
        #so we start by going over all the pos that apply to the word
        for pos in wordDict.get(word).keys():
            print pos
            #and then we confirm that it is a pos that can follow the previous pos
            if prevpos in posDict.get(pos).previousPOS.keys():
                #once we've confirmed, we can begin calculations
                #first calculate the probability that prevpos preceeds pos -- this is equal to the probability that this pos follows
                #prevpos times the probability calculated for prevPos
                probWordIsPOS = float(wordDict.get(word).get(pos))/posDict.get(pos).numOccurances
                probPrevposPreceeds = posDict.get(pos).previousPOS.get(prevpos) * lastGenerated.get(prevpos) * probWordIsPOS
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

    #we have the probability that each pos applies to each word
    #now we need to add those probabilities to the final array A
    for key in lastGenerated:
        #for each pos that we've calculated we need to add that probability to array A at position totalWords.index(word)
         A[key][totalWords.index(word)+1] = lastGenerated.get(key)

print tempLastGenerated
print lastGenerated

#we need to fill out the space for the "end" pos in A
#first find the pos in last generated with the highest probability
maxPrevProb = 0
posWithHighestProb = ""
for key in lastGenerated:
    if lastGenerated.get(key) > maxPrevProb:
        maxPrevProb = lastGenerated.get(key)
        posWithHighestProb = key

#now calculate the probability that end follows that pos
probWordPreceedsEnd =  posDict.get("end").previousPOS.get(posWithHighestProb)
#and add it to A
#embed()
A["end"][numWordsLookedAt+1] = maxPrevProb * probWordPreceedsEnd

#at this point array A is filled out and we have the correct probabilities for each word/pos combo
finalDict = {}
#so for each word we have
for word in totalWords:
    indexOfWord = totalWords.index(word)+1
    #we want to look at the probability that it can be each pos
    maxProb = 0
    associatedPOS = ""
    for pos in totalPOS:
        #so we want to search A and find the pos that the word is most likely to be
        #therefore we search through all the pos at the index of the word so that we can look at the prob of the word being that pos
        probAtCurrentPOS = A[pos][indexOfWord]

        #find the pos with the max probability
        if probAtCurrentPOS > maxProb:
            maxProb = probAtCurrentPOS
            associatedPOS = pos

    #once we have the pos that this word is most likely to be, we add it to the final dictionary so that these pairings can be used for tagging
    finalDict[word] = associatedPOS

print finalDict








