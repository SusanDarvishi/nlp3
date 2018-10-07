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
A = [[None for y in range(numUniqueWords)] for x in range(numUniquePOS)]
#this array will be the backtracking trace, it will be the same size as A and will hold in each position the location of the position that should precede it
B = [[None for y in range(numUniqueWords)] for x in range(numUniquePOS)]


#want to set the first column probabilities to 0 except the probability for start because there is a 100% chance that start is at the beginning
#of the sentence and a 0% chance that anything besides start begins a sentence
for i in range(numUniquePOS):
	A[i][0] = 0

positionOfStart = totalPOS.index("start")
A[positionOfStart][0] = 1

#embed()

#this next set of for loops will fill out both array A and array B
#array A will hold the probabilities for each circumstance, and B will hold the backtrack path

lastGenerated = {"start":1}
tempLastGenerated = {}

#begin by looking at each word
for word in totalWords:

	probEachPOSFollowingPrev = {}
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
				probPrevposPreceeds = posDict.get(pos).previousPOS.get(prevpos) * lastGenerated.get(prevpos)
				
				#add to dictionary in wider scope
				if pos in probEachPOSFollowingPrev.keys():
					#if that pos is already in that dictionary, we want to take the maximum
					probEachPOSFollowingPrev[pos] = max(probPrevposPreceeds, probEachPOSFollowingPrev.get(pos))
				else:
					#if not, just add it
					probEachPOSFollowingPrev[pos] = probPrevposPreceeds
			#else we will not calculate probability because there is no chance that the pos can follow the prevpos











