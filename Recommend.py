#Student ID: C1632338
#Program works as intended.
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import operator

#History
# ['5 5 12\n', '1 1\n', '1 2\n', '2 1\n', '2 3\n', '3 1\n', '3 2\n', '3 4\n', '4 2\n', '4 4\n', '1 2\n', '2 3\n', '5 5']

#Queries
# ['2\n', '1 2\n', '5\n', '5 1\n', '5 1 4\n', '1 3 5\n']

historyFilePath = "history2.txt"
queriesFilePath = "queries2.txt"

historyFileHeader = open(historyFilePath, "r") #Open file.
y = historyFileHeader.readlines() #read top line
v = y[0].split() #Get 0 index of the top line after splitting it.
totalTransactions = v[2]
totalTransactions = int(totalTransactions) #Value of total transactions, got from the file.

totalItems = v[1]
totalItems = int(totalItems) #Total number of items, got from the file.

totalCustomers = v[0]
totalCustomers = int(totalCustomers) #Total number of customers, got from the file.


itemDict = {} #To store all the items
historyList = [] #To store tehe history.

historyFileHeader.close()

historyFile = open(historyFilePath, "r")
next(historyFile, None) #Skip the header.

theTransactions = [] #Store each transaction that occurs.

#This loops through each line in history file and adds it to the list in a neat format.
for lines in historyFile:
	lines = lines.strip().split()
	theTransactions.append(lines)

#Counter to keep track of item index.
counter = 0

positiveEntries = 0

for transaction in theTransactions:
	itemID = theTransactions[counter][1]
	counter += 1
	if itemID not in itemDict: #Only adds item if it is not in the dictionary already.
		itemDict[itemID]=[0]*totalCustomers
	for customers in range(1, totalCustomers + 1):
		if int(transaction[0]) == customers and int(itemDict[itemID][customers-1])!=1:
			itemDict[itemID][customers-1]=1
			positiveEntries += 1 #Add to positiveEntries counter.

print("Positive entries: " + str(positiveEntries))

angles = {} #Dictionary to store all angles.
vectors = [] #List to store all vectors

#Function to calculate the angle.
def calc_angle(x, y, vectorOne, vectorTwo):
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos_theta = np.dot(x, y) / (norm_x * norm_y)
    theta = math.degrees(math.acos(cos_theta))
    round(theta,2) #Rounds it to two decimal places.
    angles[vectorOne +" "+vectorTwo] = theta #Adds the two vectors as index and angle as value to the dictionary.
    return theta

sumOfTheAngle = 0
for vectorOne in itemDict:
	v1 = np.array(itemDict.get(str(vectorOne)))
	vectors.append(v1)
	for vectorTwo in itemDict:
		if vectorTwo>vectorOne:
			sumOfTheAngle += calc_angle(itemDict[vectorOne], itemDict[vectorTwo], vectorOne, vectorTwo) #Adds to counter.

#print("Lenth of itemDict: " + str(len(itemDict)))

#print(vectors)
#print(angles)

averageAngle = round(sumOfTheAngle/len(angles),2)
print("Average angle: " + str(averageAngle))

historyFile.close() #Close the file after opening it.

theQueries = []

queryFile = open(queriesFilePath, "r")
for allQueries in queryFile: #Loops through shopping basket / queries file.
	allQueries = allQueries.strip().split() #Makes it into a nice format, without "" or []
	theQueries.append(allQueries) #Stores each value of shopping basket in theQueries.


for individualQueries in theQueries:
	print("Shopping cart:", *individualQueries) #Prints the items in the shopping cart for this loop of the file.
	minimumAngle="0"
	recommendDictionary = {}
	for products in individualQueries:
		anglesThatMatch = []
		IDofAnglesThatMatch=[]
		tempList=[]
		for obj in range(1, totalItems + 1): #Loops through 1 --> totalItems number of times.
			if int(products)>obj and str(obj) not in individualQueries:
				tempList.append(angles.get(str(obj) +" "+products)) #Adds angle that corresponds with certain query index to a temp list.
				IDofAnglesThatMatch.append(obj)
			elif obj >int(products) and str(obj) not in individualQueries:
				tempList.append(angles.get(products +" "+str(obj))) #Adds angle that corresponds with certain query index to a temp list.
				IDofAnglesThatMatch.append(obj)

		demo = 4.1 #Example data used to compare
		for angle in tempList:
			anglesThatMatch.append(angle)

		#print(tempList)
		#print(anglesThatMatch)
		del anglesThatMatch[-1] #Removes None type value from end of the list.
		#print(anglesThatMatch)
		minimumAngle = min(anglesThatMatch) #Finds the minimum angle in the list storing them for this loop / shopping basket.

		if minimumAngle==90: #If it equals 90 degrees, its not a small enough angle to be a match/
			print("Item: "+ str(products)+ " no match")
		else: #This is if it is a smaller than 90 degrees angle, it has a match!
			print("Item: "+ str(products)+ ";", "match: "+ str(IDofAnglesThatMatch[anglesThatMatch.index(minimumAngle)])+ "; "+ "angle: "+ str(round(minimumAngle,2)))		
			recommendDictionary[str(IDofAnglesThatMatch[anglesThatMatch.index(minimumAngle)])] = minimumAngle #Adds dictionary value to a temp list so it can be displayed for this loop.
		
		sortedrecommendDictionary = sorted(recommendDictionary.items(), key=operator.itemgetter(1)) #Sorts the recommened items from most recommened to least.
		#print(anglesThatMatch)

	#This bit prints the recommened bit if it has any values in the temp rec_list.
	rec_list = [x[0] for x in sortedrecommendDictionary] 
	if rec_list == ['1']:
		print("Recommend: ")
	else:
		print("Recommend:", " ".join(rec_list))

queryFile.close() #Close the file after opening it.