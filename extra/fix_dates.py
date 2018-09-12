import csv

feature = []
with open("../data/games/feature_data_2018_prod.csv", 'r') as file:
	reader = csv.reader(file)
	i = 0

	for row in list(reader):
		feature.append(row)

game = []
with open("../data/games/game_data_2018.csv", 'r') as file:
	reader = csv.reader(file)
	i = 0

	for row in list(reader):
		game.append(row)

a = zip(game, feature)

final = []
for items in a:
	final.append(items[1]+[items[0][1]])


with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(final)