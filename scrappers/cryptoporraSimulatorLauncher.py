from cryptoporraSimulator import CryptoporraSimulator
def main():
	cryptoporraSimulator = CryptoporraSimulator() 
	while True :
		cryptoporraSimulator.simulation_step()
if __name__ == "__main__":
	main()
