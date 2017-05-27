
# def sumFunction(x):
# 	terminal = x
# 	listOfNum = range(1, x + 1)
# 	total = 0
# 	for y in listOfNum:
# 		total = y + total
# 	print(total)
#
# sumFunction(1000000)
#
#
# def revSumFunction(x):
# 	potatosList = range(x, 101)
# 	total = 0
# 	for potatos in potatosList:
# 		total = potatos + total
# 	print(total)
#
# revSumFunction(5)

def myCount(x, y):
	# Error checking: which one value is greater than the other
	if x > y:
		#putting in a list with the range
		xList = range(y, x)
		#Making the starting value the lower value
		value = y
		for ys in xList:
			#having it count up one each time
			value = value + 1
			print(int(value))
			#Checking odd or even
			R = value % 2
			if R == 1:
				print('odd')
			elif R == 0:
				print('even')
			#Ending the function when it gets to y
			if value == x:
				return
			else:
				#Just seperating it out so I know what is being assigned odd or even
				print('***')
	elif y > x:
		yList = range(x, y)
		value = x
		for xs in yList:
			value = value + 1
			print(int(value))
			R = value % 2
			if R == 1:
				print('odd')
			elif R == 0:
				print('even')
			if value == y:
				return
			else:
					#Just seperating it out so I know what is being assigned odd or even
				print('***')

myCount(15,10)

def countBetween(x , y):
	lower = min(x, y)
	upper = max(x, y) + 1

	myRange = range(lower, upper)
	for number in myRange:
		if number % 2 == 1:
			print(str(number) + ' is odd')
		else:
			print(str(number) + ' is even')
countBetween(10, 29)

class Band(object):
	def __init__(self):
		self.name = 'Fall Out Boy'
		self.genre = 'Rock'
		self.members = ['Pete Wence','Patrick Stump','Andy Burnell','Joe']
		self.instruments = ['Vocals', 'Guitar', 'Base', 'Drums']
fallOutBoy = Band()
print(fallOutBoy.name)
print(fallOutBoy.members)

class Schools(object):
	def __init__(self, name, classes):
		print('Created School')
		self.name = name
		self.classes = classes

	def checkClass(self, x):
		print('Running check class on list ' + str(self.classes)
		for myClass in self.classes:
			print(myClass)
			if x == myClass:
				print(str(x) + ' is a class at ' + self.name)

BerkeleyHigh = Schools('BerkeleyHigh', ['math', 'science', 'history'])
BerkeleyHigh.checkClass('math')
MariaCorea = Schools('Maria Coreo', ['art', 'english', 'history'])

#Excersizes
#1 - create a class of name city, it will have a name, population, and a state
class City(object):
	def __init__(self): #add value for name, population, city, and state

	#add a function that checks to see whether the city has more than a million people
	def isBigCity(self):

#2 - create a class for a calculator takes 2 numbers and can, count between them, divide them, add them, and subtrcat them
class Calculator(object):
	def __init__(self): #add values for 2 numbers

	def countBetween(self):

	def addNumbers(self):

	def subtractNumbers(self):

	def divideNumbers(self):

#3 - create a class for a rock, paper, scissors game
class RockPaperScissors(object):
	def __init__(self, type): #pass in whether it is 'rock', 'paper', or 'scissors'

	def playGame(self, player2): #create a function that plays the game and compares it against another object


# def saleCalculator(medicine, population, price, prevalance):
# 	#at some point add time
# 	sales= population * (prevalance / 100) * price
# 	print(medicine +', $' + str(int(sales))+ ' revenue')
# 	return(sales)
#
# def getUserInputs():
# 	ammountOfUserInputs = int(input('How many medicines do you want to input?: '))
# 	listOfMedicines = range(1, ammountOfUserInputs + 1)
# 	total = 0
# 	for medicineNumber in listOfMedicines:
#
# 		medicine = input('What is this medicine named: ')
# 		population = input('What is the total population: ')
# 		price = input('What is the price?: ')
# 		prevalance = input('What is the prevalance (in total percent?): ')
# 		if int(prevalance) > 100:
# 			prevalance = input('please, input a percent below 100%')
# 		sales = saleCalculator(medicine, int(population), int(price), int(prevalance))
# 		total = round(total + sales, 2)
# 	print('total revenue is $' + str(total))
#
# # getUserInputs()
