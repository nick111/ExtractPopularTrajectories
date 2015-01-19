# coding: utf-8

# Usage
# python3 src/cut_json/cutting_jsons.py cutting_list_2013_11.txt 2013,10,31,19 2013,11,30,19 2013_11 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2013_12.txt 2013,11,30,19 2013,12,31,19 2013_12 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2014_01.txt 2013,12,31,19 2014,1,31,19 2014_01 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2014_02.txt 2014,1,31,19 2014,2,28,19 2014_02 9

# python3 src/cut_json/cutting_jsons.py cutting_list_2014_03.txt 2014,2,28,19 2014,3,31,19 2014_03 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2014_04.txt 2014,3,31,19 2014,4,30,19 2014_04 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2014_05.txt 2014,4,30,19 2014,5,31,19 2014_05 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2014_06.txt 2014,5,31,19 2014,6,30,19 2014_06 9
# python3 src/cut_json/cutting_jsons.py cutting_list_2014_07.txt 2014,6,30,19 2014,7,31,19 2014_07 9

# python3 src/cut_json/cutting_jsons.py cutting_list_2013_1105.txt 2013,11,4,19 2013,11,5,19 2013_1105 9

import json
import sys
import gzip
import calendar
import datetime

param = sys.argv


# 第一引数：　読み込みファイルのリスト
files_list = open('data/cut_json/cutting_list/' + param[1],'r')

# 第二引数：　収集開始日時（世界標準時間でYYYY,MM,DD,HH。それぞれMとDとHは一桁可）
start_datetime = datetime.datetime(int(param[2].split(',')[0]), int(param[2].split(',')[1]), int(param[2].split(',')[2]), int(param[2].split(',')[3]))

# 第三引数：　収集終了時（世界標準時間でYYYY,MM,DD,HH。それぞれMとDとHは一桁可。時間は17とすると17:59までとる）
end_datetime = datetime.datetime(int(param[3].split(',')[0]), int(param[3].split(',')[1]), int(param[3].split(',')[2]), int(param[3].split(',')[3]))

# 第四引数：　出力するファイルに挟み込む名称
fw_path = 'result/cut_json/cut_' + param[4] +'_out.json'

# 第五引数：　時間に何時間足すか（日本時間に直すなら9）
add_time = int(param[5])

# 最初の日本時間
start_time = (add_time + int(param[2].split(',')[3])) % 24

for file_name in files_list:
	afile = gzip.open('data/cut_json/json/' + file_name.rstrip("\n"),'r')
	num_none_coord = 0
	value_error_count = 0
	key_error_count = 0
	for line in afile:
		try:
			line = str(line.decode('utf-8'))
			tweet = json.loads(line.split('\t')[1])
		except ValueError:
			value_error_count = value_error_count + 1
			continue
		if tweet["coordinates"] is None:
			num_none_coord = num_none_coord + 1
			continue
		hour = int(tweet["created_at"].split(' ')[3].split(':')[0])
		day = int(tweet["created_at"].split(' ')[2])
		month = tweet["created_at"].split(' ')[1]
		year = int(tweet["created_at"].split(' ')[5])
		for month_i, month_name in enumerate(calendar.month_abbr):
			if month == month_name:
				month = month_i
				break
		tweet_datetime = datetime.datetime(year, month, day,hour)
		if start_datetime <= tweet_datetime < end_datetime:
			tweet_datetime = tweet_datetime + datetime.timedelta(hours=add_time)
			relative_datetime = tweet_datetime - datetime.timedelta(hours=start_time)
			fw = open(fw_path, 'a')
			try:
				t = {"user_id" : tweet["user"]["id"], "coordinates": tweet["coordinates"]["coordinates"], "datetime": str(tweet_datetime),"relative_datetime": str(relative_datetime), "tweet_id":tweet["id"]}
			except KeyError:
				key_error_count = key_error_count + 1
				continue
			fw.write(json.dumps(t))
			fw.write('\n')
			fw.close
	afile.close()
	print(file_name.rstrip("\n") +": " + str(num_none_coord) + "  :  " + str(value_error_count) + "  :  "  + str(key_error_count))
	print(str(datetime.datetime.now()))
files_list.close()





