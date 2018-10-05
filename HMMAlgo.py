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

previous = ["start"]
tempPrevious = []

#look at each word
for word in totalWords:
	probsForThisPosition = []

	#look at all of the parts of speech that can apply to that word
	for pos in wordDict.get(word):
		tempPrevious.append(pos)

		#look at the probability that each part of speech follows the previous parts of speech
		probFollowingPrevPos = 0
		for prevpos in previous:
			#here we will look at each pos that may preceed the pos of the word we're looking at
			followingProbabilities = posDict.get(pos).previousPOS
			print followingProbabilities
			probFollowingPrevPos = followingProbabilities.get(prevpos)
			# print pos
			# print prevpos
			# print probFollowingPrevPos
		
		#now we have the probability that the pos we're looking at follows one of the previous pos
		#now we want to multiply that by the probability that the pos is a given word
		
	tempPreviousPOS = []





