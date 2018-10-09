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

    print ("WORDDICT ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print (wordDict)

    print

    print("POSDICT ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for key in posDict.keys():
        print(key, posDict.get(key).numOccurances, posDict.get(key).previousPOS)
