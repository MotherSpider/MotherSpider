import datetime
import nutchpy
import os
import sys
import time
import re
import commands


crawlFolder = ""
crawlDbPath = ""
linkDbPath = ""
segmentsPath = ""
statisticsPath = ""

logFile = ""
fetchedFile = ""
unFectchedFile = ""
goneFile = ""
redirTempFile = ""
redirPermFile = ""
notModifedFile = ""
duplicateFile = ""
imageFile = ""

count1 = 0;
count2 = 0;
count3 = 0;
count4 = 0;
count5 = 0;
count6 = 0;
count7 = 0;
totalImages = 0;
totalRecordCount = 0;
counts = [totalRecordCount, count1, count2, count3, count4, count5, count6, count7, totalImages]
files = []

nutchFolder = ""

def cleanup():
	printToFile(logFile, "Parse Completed")
	for count in range(9):
		printToFile(files[count], "Total: " + str(counts[count]), False)
		printToFile(files[count], "---------------------------------------------------------------")
		files[count].close()

def parse():
	printToFile(logFile, "Parse Started", False)
	
	seq_reader = nutchpy.sequence_reader
	nodePath = crawlDbPath + "/current/part-00000/data" 
# 	records = seq_reader.count(nodePath)
# 	print records
	
	records = seq_reader.read_iterator(nodePath,0,False)
	for rec in records:
		global totalRecordCount, totalImages
		totalRecordCount += 1
		url = ""
		try:
			url = str(rec[0])
		except UnicodeEncodeError:
			printToFile(logFile, "UnicodeEncodeError in record number " + str(totalRecordCount))
			continue
		except:
			printToFile(logFile, "Unknown Error in record number " + str(totalRecordCount))
			
		data = str(rec[1]).split('Metadata:')
		result = re.findall(".+[:]{1}.+[\n]{1}", data[0])
		resultDic = {}
		for r in result:
			r = r.split(":")
			resultDic[r[0]] = r[1][:-1]
		metadata = data[1]
		printToFile(logFile, metadata)
		if 'Content-Type=image' in metadata:
			totalImages += 1
			printToFile(imageFile, url)

		status = resultDic['Status'].split(' ')
		statusCode = int(status[1])
		
		global counts, files
		counts[statusCode] += 1
		
		printToFile(files[statusCode], url+"\n", False)
		printToFile(logFile, [url,status[2]])
# 	segments = os.listdir(segmentsPath)
# 	segmentsCount = len(segments)
# 	printToFile(logFile, "Total number of segments: " + str(segmentsCount))
# 	
# 	segCurrentCount = 0
# 	for segment in segments:
# 		segCurrentCount = segCurrentCount + 1
# 		printToFile(logFile, "---------------------------------------------------------------")
# 		printToFile(logFile, "Parsing segment: " + segment)
# 		printToFile(logFile, "Segment segCurrentCount: " + str(segCurrentCount))
# 		printToFile(logFile, "Segments remaining: " + str(segmentsCount - segCurrentCount))
# 		printToFile(logFile, "---------------------------------------------------------------")
	
def createFiles():
	global files, logFile, fetchedFile, unFectchedFile, goneFile, redirTempFile, redirPermFile, notModifedFile, duplicateFile, imageFile
	logFile = open(statisticsPath + "/log", "w")
	unFectchedFile =  open(statisticsPath + "/unfetched", "w") #1
	fetchedFile =  open(statisticsPath + "/fetched", "w") #2
	goneFile = open(statisticsPath + "/gone", "w") #3
	redirTempFile = open(statisticsPath + "/redirTemp", "w") #4
	redirPermFile = open(statisticsPath + "/redirPerm", "w") #5
	notModifedFile = open(statisticsPath + "/notModified", "w") #6
	duplicateFile = open(statisticsPath + "/duplicate", "w") #7
	imageFile = open(statisticsPath + "/images", "w") #7
	files = [logFile,  unFectchedFile, fetchedFile, goneFile, redirTempFile, redirPermFile, notModifedFile, duplicateFile, imageFile]


def createStatsDir():
	print "Cleaning/Creating statistics directory"
	if not os.path.exists(statisticsPath):
		os.chmod(crawlFolder, 0777)
		os.makedirs(statisticsPath, 0777)
	else:
		os.chmod(crawlFolder, 0777)
		os.system("rm -rf " + statisticsPath + "/*")

def printToFile(fd, data, flag=True):
	if fd == logFile:
		if flag == True:
			fd.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S %f') + ": Analysing - " + str(data) + "\n")
		else:
			fd.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S %f') + ": " + str(data))
	elif flag == True:
		fd.write(str([data]))
	else:
		fd.write(str(data))
	print str(data) + "\n"

if __name__ == '__main__':
	crawlFolder = sys.argv[1]
	crawlDbPath = crawlFolder + "/crawldb";
	linkDbPath = crawlFolder + "/linkdb";
	segmentsPath = crawlFolder + "/segments";
	statisticsPath = crawlFolder + "/statistics"
	
	createStatsDir()
	
	createFiles()

	parse()

	cleanup()
