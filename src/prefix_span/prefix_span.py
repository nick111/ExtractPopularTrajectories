# coding: utf-8

# Usage
# extract_trajectories.pyで生成されたファイルから、prefixspan処理を行う。
# 経路が含むポイント数が第１引数以上になるものに限るようにし、各経路が第２引数以上の頻度があるものに限る。
# python3 src/prefix_span/prefix_span.py 3 20

import json
import sys
import glob
import calendar
import datetime
import os

param = sys.argv
current_time = datetime.datetime.today()

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

def prefixSpan(front_list_val, rear_list_val):
	global tr_dict
	for i_group_id in range(max_group_id):
		num_i = 0
		new_front = front_list_val
		new_front.append(i_group_id)
		for rear_val in rear_list_val:
			if i_group_id not in rear_val:
				continue
			else:
				num_i += 1
				index = rear_list_val.index(num_i) + 1
				if not len(rear_list_val) == index:
					new_rear = rear_list_val[index:]
					prefix_span(new_front, new_rear)
		if not len(new_front) < 2:
			tr_dict[list2String(new_front)] = num_i


least_num_point = int(param[1])
least_num_trajectory = int(param[2])

directory_path = 'result/prefix_span/result_' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute)
fw_path = directory_path + '/prefix_span.json'
fr_path = 'data/prefix_span/trajectories/trajectories.json'

tr_dict = dict()
front_list = []
rear_list = []


fr = open(fr_path,'r')
max_group_id = 0
for line in fr:
	tr = json.loads(line)
	for i in range(tr["number"]):
		rear_list.append(tr["trajectory"])
		front_list.append([])
	for point in tr["trajectory"]:
		if max_group_id < int(point):
			max_group_id = int(point)



