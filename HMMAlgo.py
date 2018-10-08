from IPython import embed

class posObject:
    numOccurances = -1
    previousPOS = {}

    def __init__(self, numOccurances, previousPOS):
        self.numOccurances = numOccurances
        self.previousPOS = previousPOS

    def updatePreviousPOS(key, value):
        self.previousPOS[key] = value

#the following dictionaries and arrays are expected output from parsing algorithm
wordDict = {"fish": {"noun": 8, "verb": 5}, "sleep": {"noun": 2, "verb": 5}}
posDict = {"noun": posObject(10, {"noun":0.1, "verb":0.2, "start":0.8}), "verb": posObject(10, {"noun":0.8, "verb":0.1, "start":0.2}), "start": posObject(1, None), "end": posObject(1, {"noun":0.1, "verb":0.7})}

totalWords = ["fish", "sleep"]
totalPOS = ["noun", "verb", "start", "end"]



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
numWordsLookedAt = 0

#begin by looking at each word
for word in totalWords:
	#look at all the pos that can preceed that word
	for prevpos in lastGenerated.keys():
		#now we want to try to find the pos that can apply to word that can also follow prevpos
		#so we start by going over all the pos that apply to the word
		for pos in wordDict.get(word).keys():
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

	#increment the number of words we've addressed at the end of the word for loop
	numWordsLookedAt += 1

	#we have the probability that each pos applies to each word
	#now we need to add those probabilities to the final array A
	for key in lastGenerated:
		#for each pos that we've calculated we need to add that probability to array A at position totalWords.index(word)
		 A[key][totalWords.index(word)+1] = lastGenerated.get(key)

	#if we have addressed all of the unique words, we need to fill out the space for the "end" pos in A
	if numWordsLookedAt == numUniqueWords:
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
