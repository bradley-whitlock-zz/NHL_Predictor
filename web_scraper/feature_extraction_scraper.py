#import requests
#from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display

from utils.logger import log

SEASON_START_DATE = '2017-09-01'
data = ["2017-10-07","Edmonton Oilers","Vancouver Canucks","2","3",""]

def load_team_ids():
	with open("data/teams/team_ids.json") as f:
		return json.load(f)

def str_to_file(body, out_file_name="test.txt"):
	with open("{}".format(out_file_name),"w+") as my_file:
		my_file.write(body)

def load_game_data(file_year):
	with open("data/games/game_data_{}.csv".format(file_year), 'r') as file:
		reader = csv.reader(file)
		return  list(reader)

def get_season_start(year):
	return str(year-1) + "-09-01"

def feature_scraper(year=2018, num_years=1):
	# Load the TEAM IDS such that the URL for nhl.com can be created
	TEAMS = load_team_ids()

	# Read CSV of game data, this is necessary for the games
	GAME_DATA = load_game_data(year)
	GAME_DATA = GAME_DATA[1:]

	SEASON_START_DATE = get_season_start(year)

	driver = webdriver.Safari()

	# Process each game
	for GAME in GAME_DATA:
		try: 
			url = "http://www.nhl.com/stats/team?aggregate=1&reportType=game&dateFrom={season_start}&" \
				  "dateTo={prev_day}&gameType=2&playerPlayedFor=team.{team_id}&filter=gamesPlayed,gte,1&sort=points,wins" \
				.format(season_start=SEASON_START_DATE, prev_day=GAME[0], team_id=TEAMS[GAME[1]])

			log.info("Fetching URL: ", url)
			#display = Display(visible=0, size=(800, 600))
			#display.start()

			
			driver.get(url)
			facts = driver.find_elements_by_class_name("rt-td")

			dimensions = driver.find_elements_by_class_name("rt-header-cell")

			if len(facts) != len(dimensions):
				log.error("WebScraping Error: len(facts)={facts} len(dimensions)={dimensions}".format(facts=len(facts), dimensions=len(dimensions)))
				raise Exception("WebScraping Error: The number of dimensions and facts for game data on nhl.com does not equal")

			if len(facts) == 0 or len(dimensions) == 0:
				log.error("WebScraping Error: Game Data: {}".format(data))
				raise Exception("WebScraping Error: No data for game on nhl.com".format(data))

				features_to
			for fact, dim in zip(facts, dimensions):
				print (fact.text, dim.text)
		except KeyError as err:
			driver.quit()
			raise KeyError(err)

	driver.quit()
		#display.stop()


#prev_day = (datetime.strptime(data[0], '%Y-%m-%d') - timedelta(days=1)).strftime("%Y-%m-%d")

