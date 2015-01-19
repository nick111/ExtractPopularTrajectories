# coding: utf-8

# Usage
# cutting_jsons.pyで生成されたjsonに対し、一日一定数以上１人によってtweetされたtweet群を抜き出す。
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 4

import json
import sys
import glob
import calendar
import datetime


param = sys.argv
current_time = datetime.datetime.today()

cut_jsons = glob.glob('data/reduce_jsons_4_trajectories/cut_jsons/*')
fw_path = 'result/reduce_jsons_4_trajectories/' + 'reduce_jsons_4_trajectories' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute) + '.json'
fr_holiday = open('data/reduce_jsons_4_trajectories/holiday/holiday_list.txt','r')

least_tweet_num = int(param[1])

print("counting the daily number of each user's tweets")
print(str(datetime.datetime.today()))

user_dict = dict()

for cut_json in cut_jsons:
	print(cut_json)
	print(str(datetime.datetime.today()))
	fr = open(cut_json,'r')
	for line in fr:
		tweet = json.loads(line)
		if tweet["user_id"] not in user_dict:
			user_dict[tweet["user_id"]] = dict()
		if tweet["relative_datetime"].split(' ')[0] not in user_dict[tweet["user_id"]]:
			user_dict[tweet["user_id"]][tweet["relative_datetime"].split(' ')[0]] = 1
		else:
			user_dict[tweet["user_id"]][tweet["relative_datetime"].split(' ')[0]] += 1


print("outputting")
print(str(datetime.datetime.today()))

in_num = 0
out_num = 0

for cut_json in cut_jsons:
	print(cut_json)
	print(str(datetime.datetime.today()))
	fr = open(cut_json,'r')
	for line in fr:
		tweet = json.loads(line)
		in_num += 1
		if user_dict[tweet["user_id"]][tweet["relative_datetime"].split(' ')[0]] >= least_tweet_num:
			out_num += 1
			if tweet["relative_datetime"].split(' ')[0] not in holidays:
				tweet.update({"day_class": 'workday'})
			else:
				tweet.update({"day_class": 'holiday'})
			fw = open(fw_path, 'a')
			fw.write(json.dumps(tweet))
			fw.write('\n')
			fw.close

print('in: ' + str(in_num) + '   out: ' + str(out_num))
