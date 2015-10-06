import sys
import re

filename = sys.argv[1]

fd = open(filename, "r")
fdR = open(filename+"Reasons", "w")
stats = {}

for line in fd:
	output = []
	key = ""
	firstSplit = line.split("failed with: ")
	output.append(firstSplit[0].split(" ")[8])
	secondSplit = re.split(",\s|:\s",firstSplit[1])
	if "Http code=" in secondSplit[0]:
		output.append(secondSplit[0])
		key = secondSplit[0]
	else:
		output.append(secondSplit[0])
		key = secondSplit[0]
		if len(secondSplit) > 1 and "java.net.UnknownHostException" not in secondSplit[0]:
			output.append(secondSplit[1])
			key += ": " + secondSplit[1]
	if "\n" in key:
		key = key[:-1]
	stats.setdefault(key,0)
	stats[key] = stats[key] + 1
	fdR.write(str(output) + "\n")
	print output
print stats
fdR.write(str(stats) + "\n")
fd.close()
fdR.close()
