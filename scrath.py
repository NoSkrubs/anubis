
def sumFunction(x):
	terminal = x
	listOfNum = range(1, x + 1)
	total = 0
	for y in listOfNum:
		total = y + total
	print(total)

sumFunction(1000000)


def revSumFunction(x):
	terminal = x
	potatosList = range(x, 101)
	total = 0
	for potatos in potatosList:
		total = potatos + total
	print(total)

revSumFunction(5)



def saleCalculator(medicine, population, price, prevalance):
	#at some point add time
	sales= population * (prevalance / 100) * price
	print(medicine +', $' + str(int(sales))+ ' revenue')
	return(sales)

def getUserInputs():
	ammountOfUserInputs = int(input('How many medicines do you want to input?: '))
	listOfMedicines = range(1, ammountOfUserInputs + 1)
	total = 0
	for medicineNumber in listOfMedicines:

		medicine = input('What is this medicine named: ')
		population = input('What is the total population: ')
		price = input('What is the price?: ')
		prevalance = input('What is the prevalance (in total percent?): ')
		if int(prevalance) > 100:
			prevalance = input('please, input a percent below 100%')
		sales = saleCalculator(medicine, int(population), int(price), int(prevalance))
		total = round(total + sales, 2)
	print('total revenue is $' + str(total))

# getUserInputs()
