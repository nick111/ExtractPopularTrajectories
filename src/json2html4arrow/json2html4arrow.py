# coding: utf-8

# Usage arrows_out.pyで作ったファイルをもとにhtmlファイルを生成する
# 	
# python3 src/json2html4arrow/json2html4arrow.py

import json
import sys
import calendar
import datetime
import math

param = sys.argv
current_time = datetime.datetime.today()

fr_header = open('data/json2html4arrow/header/header.html','r')
fr_footer = open('data/json2html4arrow/footer/footer.html','r')
fr_arrows = open('data/json2html4arrow/arrows_out/arrows_out.json','r')
fw_path = 'result/json2html4arrow/' + 'json2html4arrow' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '_' + str(current_time.minute) + '.html'

fw = open(fw_path, 'a')
fw.write(fr_header.read())
fw.close

for line in fr_arrows:
	fw  = open(fw_path, 'a')
	fw.write(line + ',' + '\n')
	fw.close

fw = open(fw_path, 'a')
fw.write(fr_footer.read())
fw.close
