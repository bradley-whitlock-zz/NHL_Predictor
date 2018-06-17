import fire

from web_scraper.scraper import scrape_data
#from model.nhl_predictor import extract_features
from utils.logger import log

class Predictor(object):
	
	def get_game_data(self, year=2018, num_years=10):
		return scrape_data(data="game", year=year, num_years=num_years)

	def get_player_data(self, year=2018, num_years=10):
		return scrape_data(data="player", year=year, num_years=num_years)

if __name__ == '__main__':
	fire.Fire(Predictor)
