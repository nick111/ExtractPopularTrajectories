# coding: utf-8

# Usage
# cutting_jsons.pyで生成されたjsonに対し、一日一定数以上１人によってtweetされたtweet群を抜き出す。
# 第１引数でその一定数を指定。第２引数はミーンシフト収束半径。連続してこの範囲に収まるツイートがあった場合は無視する．
# 第２・第３・第４は任意だが、取得データを絞る条件。
# 第２が平日か休日か、第３・第４はrelative_datetimeでの開始と終了時間（0と3を指定したら0:00〜3:59、標準時間では4:00〜7:59）
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 4 10.0
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 4 10.0 0 5 8
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 4 10.0 0 0 5
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 4 10.0 0 13 19
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 20 5000.0
# python3 src/reduce_jsons_4_trajectories/reduce_jsons_4_trajectories.py 10 3000.0

import json
import sys
import glob
import calendar
import datetime
import os
import math

param = sys.argv
current_time = datetime.datetime.today()

cut_jsons = glob.glob('data/reduce_jsons_4_trajectories/cut_jsons/*')

directory_path = 'result/reduce_jsons_4_trajectories/result_' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute)
fw_path = directory_path + '/reduced.json'

def latlngToDistance(lat1, lng1, lat2, lng2):
	# 定数 ( GRS80 ( 世界測地系 ) )
	GRS80_R_X   = 6378137.000000 # 赤道半径
	GRS80_R_Y   = 6356752.314140 # 極半径
	r_x = GRS80_R_X
	r_y = GRS80_R_Y
	dif_lat = math.pi * (lat1 - lat2) / 180.0
	dif_lng = math.pi * (lng1 - lng2) / 180.0
	mean_lat = math.pi * (lat1 + lat2) / 180.0 / 2
	eccentricity = math.sqrt(( r_x ** 2 - r_y ** 2 ) / ( r_x ** 2 ))
	w = math.sqrt(1 - (eccentricity ** 2) * (math.sin(mean_lat) ** 2))
	m = r_x * ( 1 - eccentricity ** 2 ) / ( w ** 3 )
	n = r_x / w
	d = math.sqrt((dif_lng * m) ** 2 + (dif_lat * n * math.cos(mean_lat)) ** 2)
	return d

location = json.load(open('data/reduce_jsons_4_trajectories/location/location.json','r'))
nouth_lat = float(location["nouth_lat"])
south_lat = float(location["south_lat"])
east_lng = float(location["east_lng"])
west_lng = float(location["west_lng"])
lat_denominator = location["lat_denominator"]
lng_denominator = location["lng_denominator"]
lat_numerator = (nouth_lat - south_lat) / lat_denominator
lng_numerator = (east_lng - west_lng) / lng_denominator


fr_holiday = open('data/reduce_jsons_4_trajectories/holiday/holiday_list.txt','r')
holidays = []
for holiday in fr_holiday:
	holidays.append(holiday.rstrip("\n"))

least_tweet_num = int(param[1])

print("counting the daily number of each user's tweets")
print(str(datetime.datetime.today()))

radius_of_convergence = float(param[2])
user_dict = dict()
abondon_tweets_id = []

for cut_json in cut_jsons:
	print(cut_json)
	print(str(datetime.datetime.today()))
	fr = open(cut_json,'r')
	for line in fr:
		tweet = json.loads(line)
		cell_lat_num = int((nouth_lat - float(tweet["coordinates"][1])) / lat_numerator)
		cell_lng_num = int((float(tweet["coordinates"][0]) - west_lng) / lng_numerator)
		if(cell_lat_num < 0 or lat_denominator <= cell_lat_num or cell_lng_num < 0 or lng_denominator <= cell_lng_num):
			continue
		if tweet["user_id"] not in user_dict:
			user_dict[tweet["user_id"]] = dict()
		if "previous_tweet" not in user_dict[tweet["user_id"]]:
			user_dict[tweet["user_id"]]["previous_tweet"] = tweet
		else:
			if radius_of_convergence > latlngToDistance(float(user_dict[tweet["user_id"]]["previous_tweet"]["coordinates"][1]), float(user_dict[tweet["user_id"]]["previous_tweet"]["coordinates"][0]), float(tweet["coordinates"][1]), float(tweet["coordinates"][0])):
				abondon_tweets_id.append(tweet["tweet_id"])
				continue
		if "number" not in user_dict[tweet["user_id"]]:
			user_dict[tweet["user_id"]]["number"] = 1
		else:
			user_dict[tweet["user_id"]]["number"] += 1

num_list = []
for user_id in user_dict:
	num_list.append(user_dict[user_id]["number"])
num_list.sort()
num_list.reverse()
thres_num = num_list[500]


print("outputting")
print(str(datetime.datetime.today()))

os.mkdir(directory_path)

in_num = 0
out_num = 0

for cut_json in cut_jsons:
	print(cut_json)
	print(str(datetime.datetime.today()))
	fr = open(cut_json,'r')
	for line in fr:
		in_num += 1
		tweet = json.loads(line)
		cell_lat_num = int((nouth_lat - float(tweet["coordinates"][1])) / lat_numerator)
		cell_lng_num = int((float(tweet["coordinates"][0]) - west_lng) / lng_numerator)
		if(cell_lat_num < 0 or lat_denominator <= cell_lat_num or cell_lng_num < 0 or lng_denominator <= cell_lng_num):
			continue
		if user_dict[tweet["user_id"]]["number"] < thres_num:
			continue
		if tweet["tweet_id"] in abondon_tweets_id:
			continue
		if user_dict[tweet["user_id"]]["number"] >= least_tweet_num:
			if len(param) > 3:
				if tweet["relative_datetime"].split(' ')[0] in holidays:
					if not param[3] == '1':
						continue
				else:
					if not param[3] == '0':
						continue
			if len(param) == 6:
				if not (int(param[4]) <= int(tweet["relative_datetime"].split(' ')[1].split(':')[0]) <= int(param[5])):
					continue
			out_num += 1
			fw = open(fw_path, 'a')
			fw.write(json.dumps(tweet))
			fw.write('\n')
			fw.close

print('in: ' + str(in_num) + '   out: ' + str(out_num))
