FILENAME = "ChinaAirportData.txt"
SID = 1700012613
with open(FILENAME, "r", encoding="utf-8") as f:
	lines = f.readlines()

lines_new = []

for line in lines:
	line = line.strip().split(",")
	n_parts = len(line)
	if n_parts > 4:
		print(f"Found misforamtted data: {line}")
		# fix line
		line[2] = line[2] + line[3] # concat string
		del line[3]
	elif any(map(lambda s: len(s) == 0, line)):
		print(f"Found line missing data: {line}")
		# Line missing data
		continue
	elif line[3] == "-100":
		print(f"Found wrong data: {line}")
		# Line missing data
		continue


	lines_new.append(line)

lines_new = map(lambda ss: ",".join(ss), lines_new)
lines_new = "\n".join(lines_new)

print(lines_new)

with open(f"{SID}_cnAirport.txt", "w", encoding="utf-8") as f:
	f.write(lines_new)

