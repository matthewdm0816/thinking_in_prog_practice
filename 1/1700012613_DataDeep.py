def parseCsv(lines):
    return [line.strip().split(",") for line in lines]


def embedCsv(lines):
    return "\n".join([",".join(list(map(str, line))) for line in lines])

def printSlash():
	print("-" * 50)

# 1)
FILENAME = "ChinaAirportData.txt"
SID = 1700012613
with open(f"{SID}_cnAirport.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# lines = [
# 	line.strip().split(",") for line in lines
# ]

lines = parseCsv(lines)

# without title
lines = [(line[1], float(line[2]), float(line[3])) for line in lines[1:]]

lines = [
    # place, 2018, 2017, ratio
    (line[0], line[1], round(line[1] / (1 + line[2] / 100) * 100) / 100, line[2])
    for line in lines
]
printSlash()
# 2)
lines_2 = sorted(lines, key=lambda line: line[2], reverse=True)
lines_2 = [(i + 1, *line[:-1]) for i, line in enumerate(lines)]
print(embedCsv(lines_2))
printSlash()

# 3)
lines_3 = sorted(lines, key=lambda line: line[1] - line[2], reverse=True)
lines_3 = [(i + 1, *line[:-1]) for i, line in enumerate(lines)]
print(embedCsv(lines_3))
printSlash()

# 4)
lines_4 = sorted(lines, key=lambda line: line[3], reverse=True)
lines_4 = [(i + 1, *line[:-1]) for i, line in enumerate(lines)]
print(embedCsv(lines_4))
printSlash()
