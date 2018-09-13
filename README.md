# NHL Game Predictor

#### This repository will implement a variety of tree based algorithms and Neural Nets to predict the outcome of NHL games.

## Scraping the data uses multiple sources:
1. www.hockey-reference.com for the game summary
2. www.nhl.com for the statistics heading into the game

### How to get data for 2017 NHL season
* Run: `python run.py get-games --season=2017`
* Then Run: `python run.py get-features --season=2017`
* The reason for having to do both:	
	* Data is scraped from 2 sources
	* 1 gets all the games of the season from hockey-reference.com
	* 1 pulls the stats leading into the game from nhl.com as this source has finer filters


### Further Readings
[Paper](http://web.uvic.ca/~afyshe/dm_projs/nhl_final_report.pdf) on similar NHL prediction application.