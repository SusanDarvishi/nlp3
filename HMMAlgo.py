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

#print "----------------------------------------------------------------------------------------"

#look at each word
for word in totalWords:
	#print "word ", word
	#look at all of the parts of speech that can apply to that word
	probWordAndFollowing = 0.0
	probForEachPOSOfWord = {}
	for pos in wordDict.get(word):
		#print "pos ", pos

		#look at the probability that each part of speech follows the previous parts of speech
		probFollowingPrevPos = 0.0
		for key in lastGenerated:
			#print "prevpos ", key
			#here we will look at each prev pos that may preceed the pos of the word we're looking at
			followingProbabilities = posDict.get(pos).previousPOS
			#print followingProbabilities
			probFollowingPrevPos = float(followingProbabilities.get(key))
			# print pos
			# print prevpos
			#print "probFollowingPrevPos ", probFollowingPrevPos
		
		#now we have the probability that the pos we're looking at follows one of the previous pos
		#now we want to multiply that by the probability that the pos is a given word
		wordOccurances = wordDict.get(word).get(pos)
		totalOccurances = posDict.get(pos).numOccurances
		probPOSIsWord = float(wordOccurances)/float(totalOccurances)
		# print wordOccurances
		# print totalOccurances
		#print "probPOSISWord ", probPOSIsWord
		probWordAndFollowing = float(probPOSIsWord * probFollowingPrevPos)

		#account for the duplicate probabilities for each pos because of preceeding pos
		if pos in probForEachPOSOfWord.keys():
			#this will allow us to make sure that we are keeping the maximum probability for each pos of each word
			probForEachPOSOfWord[pos] = max(probForEachPOSOfWord[pos], probWordAndFollowing)
		else:
			probForEachPOSOfWord[pos] = probWordAndFollowing

	print word
	print "initial probs ", probForEachPOSOfWord
	#embed()
	#now need to account for the fact that this word is following the previous pos included in lastGenerated
	#so we have to multiply these probabilities by those probabilities

	firstIterationOfLoop = True
	for prevpos in lastGenerated.keys():
		for currentpos in probForEachPOSOfWord.keys():
			#embed()
			if firstIterationOfLoop:
				print "multiplying ", lastGenerated.get(prevpos), " by ", probForEachPOSOfWord.get(currentpos)
				probForEachPOSOfWord[currentpos] = lastGenerated.get(prevpos) * probForEachPOSOfWord.get(currentpos)
				print "no choice in number kept ", probForEachPOSOfWord.get(currentpos)
			else:
				print "multiplying ", lastGenerated.get(prevpos), " by ", probForEachPOSOfWord.get(currentpos)
				probForEachPOSOfWord[currentpos] = max(probForEachPOSOfWord.get(currentpos),(lastGenerated.get(prevpos) * probForEachPOSOfWord.get(currentpos)))
				print "choosing ", max(probForEachPOSOfWord.get(currentpos),probForEachPOSOfWord.get(currentpos))
		print "currentpos prob ", probForEachPOSOfWord.get(currentpos)
		firstIterationOfLoop = False	

	print "final probs ", probForEachPOSOfWord

	#print "----------------------------------------------------------------------------------------"
	#now we have the probability for each pos of the word
	#we need to add those to last generated so the following word can account for these probabilities
	lastGenerated = probForEachPOSOfWord
	tempLastGenerated = {}





