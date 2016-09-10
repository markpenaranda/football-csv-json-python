import json 
import csv
import urllib2
import requests
import pprint
from progress.bar import Bar


from googleapiclient.discovery import build

##data = json.loads(urllib2.urlopen("http://api.football-api.com/2.0/competitions?Authorization=565ec012251f932ea4000001393b4115a8bf4bf551672b0543e35683"))

	
service = build("customsearch", "v1", developerKey=" AIzaSyD0AAmT8YreXGW5y6mv6Y2XSqsB4bEJe1s")

response = requests.get("http://api.football-api.com/2.0/standings/1204?Authorization=565ec012251f932ea4000001393b4115a8bf4bf551672b0543e35683");

data = response.json()


f = csv.writer(open("test.csv", "wb+"))
p = csv.writer(open("players.csv", "wb+"))
p.writerow(["id","created_by","created_at","first_name","last_name","team_id", "image_url"])
f.writerow(["id","created_by","created_at","name","nickname","league_id", "image_url"])

team_count = 0
for x in data:
	##print x['team_id']
	team_count = team_count + 1
	print  str(team_count) +"/"+ str(len(data));


	google_res = service.cse().list(
	      q=x['team_name'] + " badge",
	      cx='004600183681775061592:ndwbflrtpzw',
		).execute()

	# pprint.pprint(res.items)
	team_image = "";

	for items in google_res['items']:
		if 'cse_image' in items['pagemap']:
			team_image = items['pagemap']['cse_image'][0]['src']
			break
			# print que

	f.writerow([x['team_id'],"system", "2016-09-01 00:00:00+08", x['team_name'], x['team_name'],1, team_image])

	resp = requests.get("http://api.football-api.com/2.0/team/" + x['team_id'] + "?Authorization=565ec012251f932ea4000001393b4115a8bf4bf551672b0543e35683");

	team = resp.json()

	counter = 0
	bar = Bar('Processing', max=len(team['squad']))
	for pl in team['squad']:
		bar.next()
		jersey_number = pl['number']

		resp_pl = requests.get("http://api.football-api.com/2.0/player/" + pl['id'] + "?Authorization=565ec012251f932ea4000001393b4115a8bf4bf551672b0543e35683");


		player = resp_pl.json()
		


		search_query = player['lastname'] + " " + x['team_name']

		google_res = service.cse().list(
		      q=search_query,
		      cx='004600183681775061592:ndwbflrtpzw',
			).execute()

		# pprint.pprint(res.items)
		profile_image = "";

		for items in google_res['items']:
			if 'cse_image' in items['pagemap']:
				profile_image = items['pagemap']['cse_image'][0]['src']
				break
				# print que

		p.writerow([player['id'], "system", "2016-09-01 00:00:00+08", player['firstname'].encode("utf-8"), player['lastname'].encode("utf-8"), x['team_id'], profile_image])
	bar.finish()
		
