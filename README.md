# NHL Game Predictor

#### This repository will implement a variety of tree based algorithms and Neural Nets to predict the outcome of NHL games.

## Web Scraping Sources
1. [Hockey-Reference.com](www.hockey-reference.com) for the results of all games in a season.
2. [NHL.com](www.nhl.com) for the statistics on "game day".

### Ex: How to get data for 2017 NHL season
* Run: `python run.py get-games --season=2017`
* Then Run: `python run.py get-features --season=2017`
* Reason for 2 cmds	
	* Data is scraped from 2 sources mentioned above
	* 1 gets all the games of the season from hockey-reference.com
	* 1 pulls the stats leading into the game from nhl.com as this source has finer filters

## Model Selection
Random Forest implementation details

* Random Forest was chosen due to
	* Reduces the overfitting to a noisy dataset
	* Predicting NHL games is very difficult (paper below suggests 62% upper bound)
	* Easy to control depth of trees and number of estimators for feedback
* Features used ratios of *Home Team Score / Away Team Score* to couple the relevant data and simplify comparisions. It was assumed that *Home Team Score* is irrevelant alone and only provides insight when paired with *Away Team Score*
* Model was tuned to include greater Bias in the Bias-Variance tradeoff for the similar reason of avoiding overfitting. Since bagging (Bootstrap Aggregation) incetivizes deep trees, this tradeoff was monitored carefully.


### Further Readings
[Thesis](http://web.uvic.ca/~afyshe/dm_projs/nhl_final_report.pdf) on similar NHL prediction application.