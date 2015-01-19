# coding: utf-8

# Usage
# mean_shift.pyで生成されたファイルから、後続のprefixspan処理が効率的に処理できるよう、
# 日別・ユーザ別のtrajectoryを出力する
# python3 src/extract_trajectories/extract_trajectories.py

import json
import sys
import glob
import calendar
import datetime
import os

param = sys.argv
current_time = datetime.datetime.today()

directory_path = 'result/extract_trajectories/result_' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute)
fw_path = directory_path + '/trajectories.json'
fr_path = 'data/extract_trajectories/points/points.json'

def list2String(var):
	returnVal = str(var[0])
	for element in var[1:]:
		returnVal = returnVal + ',' + str(element)
	return returnVal

def string2list(var):
	returnVal = []
	for element in var.split(","):
		returnVal.append(int(element))
	return returnVal


fr = open(fr_path,'r')

user_day_trajectory_dict = dict()

for line in fr:
	tweet = json.loads(line)
	if tweet["user_id"] not in user_day_trajectory_dict:
		user_day_trajectory_dict[tweet["user_id"]] = dict()
	if tweet["relative_datetime"].split(' ')[1].split(':')[0] not in user_day_trajectory_dict[tweet["user_id"]]:
		user_day_trajectory_dict[tweet["user_id"]][tweet["relative_datetime"].split(' ')[1].split(':')[0]] = [tweet["group_id"]]
		continue
	present_tr = user_day_trajectory_dict[tweet["user_id"]][tweet["relative_datetime"].split(' ')[1].split(':')[0]]
	last_point = present_tr[-1]
	if last_point == tweet["group_id"]:
		continue
	user_day_trajectory_dict[tweet["user_id"]][tweet["relative_datetime"].split(' ')[1].split(':')[0]].append(tweet["group_id"])

trajectory_dict = dict()

for user_id in user_day_trajectory_dict:
	for day in user_day_trajectory_dict[user_id]:
		if list2String(user_day_trajectory_dict[user_id][day]) not in trajectory_dict:
			trajectory_dict[list2String(user_day_trajectory_dict[user_id][day])] = 1
		else:
			trajectory_dict[list2String(user_day_trajectory_dict[user_id][day])] += 1

os.mkdir(directory_path)

for tr in trajectory_dict.keys():
	listTr = string2list(tr)
	fw = open(fw_path, 'a')
	fw.write(json.dumps({"trajectory": listTr, "number": trajectory_dict[tr]}))
	fw.write('\n')
	fw.close




