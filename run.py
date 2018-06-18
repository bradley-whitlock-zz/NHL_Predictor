import fire

from utils.logger import log

from web_scraper.game_scraper import scrape_data
#from model.nhl_predictor import extract_features
from web_scraper.feature_extraction_scraper import feature_scraper
from web_scraper.nhl_data_to_json import team_id_parser


class Predictor(object):
	
	def get_game_data(self, season=2018, num_years=1):
		return scrape_data(data="game", year=year, num_years=num_years)

	def get_player_data(self, season=2018, num_years=1):
		return scrape_data(data="player", year=year, num_years=num_years)

	def gen_team_ids(self):
		return team_id_parser()

	def get_game_features(self, season=2018, num_years=1):
		return feature_scraper()

if __name__ == '__main__':
	fire.Fire(Predictor)
