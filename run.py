import fire

from web_scraper.game_scraper import scrape_data
# from model.nhl_predictor import extract_features
from web_scraper.feature_extraction_scraper import FeatureScraper
from web_scraper.nhl_data_to_json import team_id_parser


class Predictor(object):

    def get_games(self, season=2018, num_seasons=1):
        return scrape_data(data="games", season=season, num_seasons=num_seasons)

    def get_players(self, season=2018, num_seasons=1):
        return scrape_data(data="skaters", season=season, num_seasons=num_seasons)

    def get_points(self, season=2018, num_seasons=1):
        return scrape_data(data="standings", season=season, num_seasons=num_seasons)

    def gen_teams(self):
        return team_id_parser()

    def get_features(self, season=2018, num_seasons=1, row=0):
        feature_scraper = FeatureScraper(season=season, num_seasons=num_seasons, row=row)
        return feature_scraper.run_scraper()


if __name__ == '__main__':
    fire.Fire(Predictor)
