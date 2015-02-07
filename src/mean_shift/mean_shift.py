# coding: utf-8

# Usage
# reduce_jsons_4_trajectories.pyで生成されたファイルから、点群を抜き出し、ミーンシフト法によって、
# クラスタリングをし、各クラスタの収束点を出力する。
# 第１引数で平均を取る半径の長さをメートルで指定。第2引数で収束条件距離を指定。
# python3 src/mean_shift/mean_shift.py 100.0 10.0

import json
import sys
import glob
import calendar
import datetime
import os
import math

param = sys.argv
current_time = datetime.datetime.today()

radius_of_mean = float(param[1])
radius_of_convergence = float(param[2])

directory_path = 'result/mean_shift/result_' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute)
fw_points_path = directory_path + '/points.json'
fw_groups_path = directory_path + '/groups.json'
fr_reduced_path = 'data/mean_shift/reduced_jsons/reduced.json'

def latlngToDistance(lat1, lng1, lat2, lng2):
	# 定数 ( GRS80 ( 世界測地系 ) )
	GRS80_R_X   = 6378137.000000 # 赤道半径
	GRS80_R_Y   = 6356752.314140 # 極半径
	r_x = GRS80_R_X
	r_y = GRS80_R_Y
	dif_lat = math.pi * (lat1 - lat2) / 180.0
	dif_lng = math.pi * (lng1 - lng2) / 180.0
	mean_lat = math.pi * (lat1 + lat2) / 180.0 / 2.0
	eccentricity = math.sqrt(( r_x ** 2 - r_y ** 2 ) / ( r_x ** 2 ))
	w = math.sqrt(1.0 - (eccentricity ** 2) * (math.sin(mean_lat) ** 2))
	m = r_x * ( 1.0 - eccentricity ** 2 ) / ( w ** 3 )
	n = r_x / w
	d = math.sqrt((dif_lng * m) ** 2 + (dif_lat * n * math.cos(mean_lat)) ** 2)
	return d

def decideNextPoint(this_point):
	mean_lat = 0.0
	mean_lng = 0.0
	sum_lat = 0.0
	sum_lng = 0.0
	num_elements = 0.0
	global is_convergent
	for point in points:
		distance_between_2_points = latlngToDistance(this_point["present_point"]["lat"], this_point["present_point"]["lng"], point["present_point"]["lat"], point["present_point"]["lng"])
		if not distance_between_2_points <= radius_of_mean:
			continue
		num_elements += 1.0
		sum_lat += point["present_point"]["lat"]
		sum_lng += point["present_point"]["lng"]
		if not distance_between_2_points <= radius_of_convergence:
			is_convergent = False
	mean_lat = sum_lat / num_elements
	mean_lng = sum_lng / num_elements
	this_point["next_point"]["lat"] = mean_lat
	this_point["next_point"]["lng"] = mean_lng
	return this_point

def updatePoint(this_point):
	this_point["present_point"]["lat"] = this_point["next_point"]["lat"]
	this_point["present_point"]["lng"] = this_point["next_point"]["lng"]
	return this_point

def decideGroupID():
	global points
	current_group_id = 0
	for pointA in points:
		if "group_id" in pointA:
			continue
		pointA["group_id"] = current_group_id
		current_group_id += 1
		for pointB in points:
			if "group_id" in pointB:
				continue
			distance_between_2_points = latlngToDistance(pointA["present_point"]["lat"], pointA["present_point"]["lng"], pointB["present_point"]["lat"], pointB["present_point"]["lng"])
			if distance_between_2_points <= radius_of_convergence:
				pointB["group_id"] = pointA["group_id"]
	num_group = current_group_id
	return num_group

def decideMeansOfEachGroup():
	means_of_each_group = []
	for i in range(num_group):
		mean_point = {"group_id": i ,"lat": 0.0, "lng": 0.0, "num_points": 0}
		for point in points:
			if point["group_id"] == i:
				mean_point["lat"] += point["present_point"]["lat"]
				mean_point["lng"] += point["present_point"]["lng"]
				mean_point["num_points"] += 1
		mean_point["lat"] = mean_point["lat"] / mean_point["num_points"]
		mean_point["lng"] = mean_point["lng"] / mean_point["num_points"]
		means_of_each_group.append(mean_point)
	return means_of_each_group


print("reading file")
print(str(datetime.datetime.today()))

fr_reduced = open(fr_reduced_path,'r')
points = []
for line in fr_reduced:
	tweet = json.loads(line)
	points.append({"tweet_id": tweet["tweet_id"], "present_point": {"lat": float(tweet["coordinates"][1]), "lng": float(tweet["coordinates"][0])}, "next_point": {"lat": 0.0, "lng": 0.0}})


print("doing mean-shift")
print(str(datetime.datetime.today()))

is_convergent = False
while(is_convergent == False):
	is_convergent = True
	for i, point in enumerate(points):
		points[i] = decideNextPoint(point)
	for i, point in enumerate(points):
		points[i] = updatePoint(point)
	print(str(datetime.datetime.today()))


print("deciding the group of each point")
print(str(datetime.datetime.today()))
		
num_group = decideGroupID()


print("deciding the mean point of each group")
print(str(datetime.datetime.today()))

means_of_each_group = decideMeansOfEachGroup()


print("outputting")
print(str(datetime.datetime.today()))

os.mkdir(directory_path)

fr_reduced = open('data/mean_shift/reduced_jsons/reduced.json','r')
for i,line in enumerate(fr_reduced):
	tweet = json.loads(line)
	tweet.update({"group_id": points[i]["group_id"]})
	fw = open(fw_points_path, 'a')
	fw.write(json.dumps(tweet))
	fw.write('\n')
	fw.close

for mean in means_of_each_group:
	fw = open(fw_groups_path, 'a')
	fw.write(json.dumps(mean))
	fw.write('\n')
	fw.close

