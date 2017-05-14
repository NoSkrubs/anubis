def myFunction():
    try:
        userInput = input('Please insert integer: ')
        integer = int(userInput)
        check = integer % 2

        if check == 0:
            print('Even number')
        elif check == 1:
            print('odd number')
        else:
            print('ERROR! ' + userInput)
    except:
        myFunction()


myFunction()
