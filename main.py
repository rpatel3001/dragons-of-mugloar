import requests as req
import xmltodict
import time
import operator
import json
import numpy as np
import yaml

def make_dragon(k):
	equiv = {"attack": "scaleThickness",
			 "armor" : "clawSharpness",
			 "endurance": "fireBreath",
			 "agility": "wingStrength"}
	d = {}
	k = sorted(k.items(), key=operator.itemgetter(1), reverse=True)
	d[equiv[k[0][0]]] = k[0][1] + 2
	if k[3][1] == 0:
		d[equiv[k[1][0]]] = k[1][1] - 1
		d[equiv[k[2][0]]] = k[2][1] - 1
		d[equiv[k[3][0]]] = 0
	else:
		d[equiv[k[1][0]]] = k[1][1]
		d[equiv[k[2][0]]] = k[2][1] - 1
		d[equiv[k[3][0]]] = k[3][1] - 1

	return d

n = 0
wins = 0
log = open("mugloar.log", "a")
while True:
	game = req.get("http://www.dragonsofmugloar.com/api/game").json()
	g_id = game['gameId']
	knight = game['knight']
	del knight['name']
	weather = xmltodict.parse(req.get("http://www.dragonsofmugloar.com/weather/api/report/%s"%g_id).text)['report']
	w_code = weather['code']

	dragon = {}

	if w_code == 'NMR':
		# normal
		dragon = make_dragon(knight)
		pass
	elif w_code == 'SRO':
		# storm
		# doesn't really matter
		pass
	elif w_code == 'T E':
		# dry
		# let's get zen
		dragon['scaleThickness'] = 5
		dragon['clawSharpness'] = 5
		dragon['wingStrength'] = 5
		dragon['fireBreath'] = 5
		pass
	elif w_code == 'HVA':
		# flood
		# fire is useless, need claws
		dragon['scaleThickness'] = 5
		dragon['clawSharpness'] = 10
		dragon['wingStrength'] = 5
		dragon['fireBreath'] = 0
		pass
	elif w_code == 'FUNDEFINEDG':
		# fog
		# auto win with a live dragon
		dragon['scaleThickness'] = 5
		dragon['clawSharpness'] = 5
		dragon['wingStrength'] = 5
		dragon['fireBreath'] = 5
		pass
	else:
		print("UNKNOWN")
		print("game: " + str(game['gameId']))
		print("weather: " + w_code)
		print(weather['message'])
		print()

	if w_code != 'SRO':
		dragon = {"dragon": dragon}
	else:
		dragon = {}

	res = req.put("http://www.dragonsofmugloar.com/api/game/%s/solution"%g_id, json=dragon).json()
	print(res['message'])
	if res['status'] == 'Victory':
		wins += 1
	n += 1

	print(str(wins/n*100) + " % wins\n")
	# gameId scale claw fire wing victory
	if w_code != 'SRO':
		dragon = dragon['dragon']
		log.write('\t'.join((str(g_id), str(dragon['scaleThickness']), str(dragon['clawSharpness']), str(dragon['fireBreath']), str(dragon['wingStrength']), str(res['status'] == 'Victory'))) + '\n')
	else:
		log.write('\t'.join((str(g_id), "0", "0", "0", "0", str(res['status'] == 'Victory'))) + '\n')

