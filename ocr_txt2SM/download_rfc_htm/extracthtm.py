import re

with open('protocoltables.html', 'r') as fh:
	lines = fh.readlines()


for line in lines:
	if len(line)<10:
		continue
	matchObj = re.search( r'.*(\"\S+.htm\").*', line)
	if matchObj:
		print(matchObj.group(1))