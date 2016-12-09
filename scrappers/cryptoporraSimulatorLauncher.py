from cryptoporraSimulator import CryptoporraSimulator
def main():
	cryptoporraSimulator = CryptoporraSimulator() 
	opt = True
	while opt:
		print("""
			[Cryptoporra Simulator]
			1.- Interactive mode
			2.- Auto mode
			3.- Exit
		""")
		opt = raw_input("What mode do you want to run? ")
		if opt=="1":
			print("Interactive mode")
			intOpt = True
			while intOpt:
				print("""
			[Interactive mode]
			1.- Create a random match
			2.- Update a random match
			3.- Make a random bet
			4.- Make a random pool
			5.- Make a random user
			6.- Make a random competition
			7.- Go back
				""")
				intOpt = raw_input("What operation do you want to do? ")
				if intOpt=="1":
					cryptoporraSimulator.create_a_random_match()
					print("Random match created")
				elif intOpt=="2":
					cryptoporraSimulator.random_update_a_match()
					print("Random match updated")
				elif intOpt=="3":
					cryptoporraSimulator.make_a_random_bet()
					print("Random bet created")
				elif intOpt=="4":
					cryptoporraSimulator.make_a_random_pool()
					print("Random pool created")
				elif intOpt=="5":
					cryptoporraSimulator.make_a_random_user()
					print("Random user created")
				elif intOpt=="6":
					cryptoporraSimulator.create_a_random_competition()
					print("Random competition created")
				elif intOpt=="7":
					intOpt = False
		elif opt=="2":
			print("Auto mode (Still to be implemented)")
		elif opt=="3":
			print("Goodbye")
			exit()
		elif opt!="":
			print("Invalid option, try again")
	#while True :
	#	cryptoporraSimulator.simulation_step()
if __name__ == "__main__":
	main()
