from scrapper_la_liga_oficial.scrapperLaLigaOficial import ScrapperLaLigaOficial
def main():
	dateRange = 5
	laLigaOficialScrapper = ScrapperLaLigaOficial() 
	laLigaOficialScrapper.start_scrapping(dateRange)
if __name__ == "__main__":
	main()
