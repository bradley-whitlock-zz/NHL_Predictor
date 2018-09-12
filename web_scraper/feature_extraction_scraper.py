import json
import csv
import time
# from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from utils.logger import log


class AnyClass:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """

    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass


class FeatureScraper:
    def __init__(self, season=2018, num_seasons=1, row=0):
        self.season = season
        self.num_seasons = num_seasons
        self.row = row
        # Get the season start date based on file_name (if file name contains 2018, 2017-2018 NHL season)
        self.season_start_date = self.get_season_start(self.season)

    @staticmethod
    def load_team_ids(file_name="data/teams/team_ids.json"):
        with open(file_name) as f:
            return json.load(f)

    @staticmethod
    def load_game_data(season):
        with open("data/games/game_data_{}.csv".format(season), 'r') as file:
            reader = csv.reader(file)
            return list(reader)

    @staticmethod
    def get_season_start(season):
        return str(season - 1) + "-09-01"

    @staticmethod
    def list_to_file(content, out_file_name="unnamed_data.csv", recreate=False):
        log.info("writing data to {}".format(out_file_name))
        file_type = "a" if recreate == False else "w"

        with open("data/{}".format(out_file_name), file_type) as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerow(content)

    def scrape_game_data(self, team_id, team_name, data, timeout, driver):

        url = "http://www.nhl.com/stats/team?aggregate=1&reportType=game&dateFrom={season_start}&" \
              "dateTo={prev_day}&gameType=2&playerPlayedFor=team.{team_id}&filter=gamesPlayed,gte,1&sort=points,wins" \
            .format(season_start=self.season_start_date, prev_day=data[1], team_id=team_id)

        log.info("Fetching URL for team {} at: {}".format(team_name, url))
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        driver.get(url)

        # Set timeout for the div's to load
        page_load_timeout = 5

        # Having issues with requesting URL but old data still exists, try waiting for class
        # Cant wait for rt-td because if no game data then this class is not present
        #   Alternative: use alongside rt-noData as this is what appears when no data present
        _ = WebDriverWait(driver, page_load_timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'rt-header-cell')))
        _ = WebDriverWait(driver, page_load_timeout).until(
            AnyClass(EC.presence_of_element_located((By.CLASS_NAME, 'rt-td')),
                     EC.presence_of_element_located((By.CLASS_NAME, 'rt-noData'))))

        # The issue occurs when the page is loaded but not before parsing game, gets the old data again
        # The timeout can be increased if data not loaded successfully
        time.sleep(timeout)

        facts = driver.find_elements_by_class_name("rt-td")
        dimensions = driver.find_elements_by_class_name("rt-header-cell")

        game_data = []

        if len(facts) == 0 and len(dimensions) > 0:
            log.info("No Game Data exists, likely first game of season for {}".format(team_name))
            # Fill in team name and then fill game data with 0's
            game_data += [team_name] + [0] * (len(dimensions) - 2)
            return game_data

        elif len(facts) == 0 and len(dimensions) == 0:
            log.info(
                "WebScraping Issue: Could not properly read data from web page. len(facts): {} len(dimensions): {}".format(
                    len(facts), len(dimensions)))
            return None

        elif len(facts) != len(dimensions):
            log.error("WebScraping Error: len(facts)={facts} len(dimensions)={dimensions}".format(
                facts=len(facts), dimensions=len(dimensions)))
            raise Exception("WebScraping Error: The number of dimensions and facts for game data on nhl.com does not equal")

        # Remove the team index column from result set on nhl.com
        facts = facts[1:]
        dimensions = dimensions[1:]

        # Check to ensure that the team names are the same, Montreal Canadians can cause error with the e
        scraped_name = facts[0].text.replace("é", "e")
        if scraped_name != team_name:
            log.info("WebScraping Issue: Expected: {} got: {}".format(team_name, scraped_name))
            return None

        log.info("Successfully scraped data for {}, extracting {} features.".format(team_name, len(facts)))
        for fact, dim in zip(facts, dimensions):
            game_data.append(fact.text)

        return game_data

    def run_scraper(self):
        # Load the TEAM IDS such that the URL for nhl.com can be created
        TEAMS = self.load_team_ids()

        # Read CSV of game data, this is necessary for the games, remove the columns header
        GAME_DATA = self.load_game_data(self.season)
        GAME_DATA = GAME_DATA[1:]

        # If we do not need restart the web-scraping process, then don't insert header
        if self.row <= 0:
            # Dimensions array currently includes (in order):
            dimension_list = ["team", "gp", "w", "l", "t", "ot", "p", "gf", "ga", "s/o win", "s/o loss", "sf", "sa",
                              "ppg", "pp opp",
                              "pp%", "ts", "ppga", "pk%", "fow", "fol", "fow%"]
            prefixs = ["visitor_", "home_"]

            header = ["game_id"] + ["{}{}".format(prefix, dim) for prefix in prefixs for dim in dimension_list] + [
                "home_goals", "visitor_goals", "extra_time"]
            self.list_to_file(header, out_file_name="games/feature_data_{}.csv".format(self.season), recreate=True)

        driver = webdriver.Safari()

        # Process each game
        print (GAME_DATA)
        for GAME in GAME_DATA:
            print (self.row)
            print (GAME)
            if int(GAME[0]) < self.row:
                continue
            # Append the game ID to the file
            game_data = [GAME[0]]

            log.info("Working on Game ID: {}".format(GAME[0]))

            for team_name in [GAME[2], GAME[3]]:
                try:
                    # The team name must be parsed to an ID for the URL to nhl.com
                    team_id = TEAMS[team_name]
                    timeout = 1

                    while True:
                        data = self.scrape_game_data(team_id=team_id, team_name=team_name, data=GAME, timeout=timeout,
                                                     driver=driver)
                        if timeout > 15:
                            raise TimeoutException("Could not scrape data from nhl.com. Tried several timeouts.")
                        elif data is not None:
                            game_data += data
                            break
                        else:
                            log.info("Increasing page timeout and trying again.")
                            timeout += 3

                except KeyError as err:
                    driver.quit()
                    raise KeyError(err)
                except TimeoutException:
                    driver.quit()
                    raise TimeoutException("WebScraping Error: Took to long to load data")
                except:
                    driver.quit()
                    raise

            # Append the game results to the feature set, write to file
            # Right now, updating file for every game due to issues in the web-scraping process and method to prevent
            #   restarting upon each error
            game_data += [GAME[4], GAME[5], GAME[6]]
            self.list_to_file(game_data, out_file_name="games/feature_data_{}.csv".format(self.season))

        driver.quit()
        # display.stop()
