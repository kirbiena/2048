from twozerofoureight import Twentyfourtyeight
while True:
	print("----------")
	print("Choose ur game")
	print("1. 2048")
	
	option = (input("Please choose a game you want to play (1-)"))
	if int(option) == 1:
		gameone = Twentyfourtyeight()
		gameone.main()
	
	else:
		print("Please input a valid choice option.")
		
