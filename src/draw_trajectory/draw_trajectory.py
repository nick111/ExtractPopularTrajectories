# coding: utf-8

# Usage
# python3 src/draw_trajectory/draw_trajectory.py 

import json
import sys
import glob
import calendar
import datetime
import os

param = sys.argv
current_time = datetime.datetime.today()

directory_path = 'result/draw_trajectory/result_' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute)
fr_groups_path = 'data/draw_trajectory/groups/groups.json'
fr_trajectories_path = 'data/draw_trajectory/trajectories/trajectories.json'
fw_path = directory_path + '/arrows_out.json'

trajectories = []
groups = dict()

fr_groups = open(fr_groups_path,'r')

for line in fr_groups:
	x = json.loads(line)
	groups[x["group_id"]] = {"group_id": x["group_id"], "lat": x["lat"], "lng": x["lng"]}

fr_trajectories = open(fr_trajectories_path,'r')

arrows = []
max_size = 0
for line in fr_trajectories:
	x = json.loads(line)
	if len(x["trajectory"]) < 2:
		continue
	if max_size < x["number"]:
		max_size = x["number"]
	last_lat = groups[x["trajectory"][0]]["lat"]
	last_lng = groups[x["trajectory"][0]]["lng"]
	for y in x["trajectory"][1:]:
		arrow = {"from_lat": last_lat, "from_lng": last_lng, "to_lat": groups[x["trajectory"][0]]["lat"], "to_lng": groups[x["trajectory"][0]]["lng"], "size": x["number"]}
		arrows.append(arrow)
		last_lat = groups[y]["lat"]
		last_lng = groups[y]["lng"]

for i,arrow in enumerate(arrows):
	arrows[i]["size"] = arrows[i]["size"] / max_size


os.mkdir(directory_path)

for x in arrows:
	fw = open(fw_path, 'a')
	fw.write(json.dumps(x))
	fw.write('\n')
	fw.close
