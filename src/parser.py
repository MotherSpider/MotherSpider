import datetime
import nutchpy
import os
import sys
import time
import re

#Constants and fields used
crawlFolder = ""
crawlDbPath = ""
linkDbPath = ""
segmentsPath = ""
statisticsPath = ""

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
mimeTypes = {}

nutchFolder = ""

favIcons = "Apparent FavIcon other than icons"
thumbnails = "Apparent Thumbnails other than icons"

#File handlers
logFile = ""  #Log File
fetchedFile = "" #Fetched file to keep track of the successful fetched urls as given by the crawl status with code: 2 (db_fetched)
unFectchedFile = "" #UnFetched file to keep track of the failed urls as given by the crawl status with code: 1 (db_unfetched)
goneFile = "" #Gone file to keep track of the urls which are not available any more as given by the crawl status with code: 3 (db_gone)
redirTempFile = "" #RedirTemp file to keep track of the urls which are moved to a different location temporairly as given by the crawl status with code: 4 (db_redir_temp)
redirPermFile = "" #RedirPerm file to keep track of the urls which are moved to a different location as given by the crawl status with code: 5 (db_redir_perm)
notModifedFile = "" #NotModified file to keep track of the urls which are not modified(cookie expiration) as given by the crawl status with code: 6 (db_not_modified)
duplicateFile = "" #RedirTemp file to keep track of the urls which are duplicates as given by the crawl status with code: 7 (db_duplicate)
imageFile = "" #ImageFile to keep track of urls which are of image mimetypes

#Perform cleanup operations. 
#Print Mimetypes to image file. 
#Print total stat for each individual file.
#Close all the file handlers.
def cleanup():
	printToFile(imageFile, str(mimeTypes) + "\n", False)
	printToFile(imageFile, "Valid images count: " + str(counts[8]-mimeTypes[favIcons]-mimeTypes[thumbnails]) + "\n", False)
	printToFile(logFile, "Parse Completed")
	for count in range(9):
		printToFile(files[count], "Total: " + str(counts[count]) + "\n", False)
		printToFile(files[count], "---------------------------------------------------------------", False)
		files[count].close()

#Parse the crawled data using nutchpy.
#Write the stats to different files.
#Check for images and find mimeTypes of each image
#Check whether the image is thumbnail or favicon
def parse():
	#Start the log
	printToFile(logFile, "Parse Started", False)
	
	#Setup nutchpy sequence_reader
	seq_reader = nutchpy.sequence_reader
	nodePath = crawlDbPath + "/current/part-00000/data" 
	
	#Read the records iteratively to avoid OUT OF MEMORY issue.
	records = seq_reader.read_iterator(nodePath,0,False)

	global mimeTypes, mimeType, counts, files, favIcons, thumbnails
	mimeTypes[favIcons] = 0
	mimeTypes[thumbnails] = 0

	#Iterate over the the records
	for rec in records:
		#Initialize fields
		
		counts[0] += 1
		url = ""
		data = ""
		
		#Use exception handling in case where url is not proper to avoid exiting of the program
		try:
			#Get the url
			url = str(rec[0])
			#Get the Metadata of the file	
			data = str(rec[1]).split('Metadata:')
		except UnicodeEncodeError:
			printToFile(logFile, "UnicodeEncodeError in record number " + str(counts[0]))
			continue
		except:
			printToFile(logFile, "Unknown Error in record number " + str(counts[0]))
		
		#Get the Metadata of the file	
		data = str(rec[1]).split('Metadata:')
		result = re.findall(".+[:]{1}.+[\n]{1}", data[0])
		resultDic = {}
		for r in result:
			r = r.split(":")
			resultDic[r[0]] = r[1][:-1]
		metadata = data[1]

		#Check for image
		if 'Content-Type=image' in metadata:
			counts[8] += 1
			printToFile(imageFile, url+"\n", False)
			
			#Get the mimeType
			ext = metadata.split('\n')[1][21:]
			mimeTypes.setdefault(ext, 0)
			mimeTypes[ext] = mimeTypes[ext] + 1

			#Check for favicon and thumbnail
			if "favicon" in url and "icon" not in ext:
				mimeTypes[favIcons] = mimeTypes[favIcons] + 1
			if ("thumbnail" in url or "thumb" in url) and "icon" not in ext:
				mimeTypes[thumbnails] = mimeTypes[thumbnails] + 1				
		
		#Get the status from nutch crawl and update the count	
		status = resultDic['Status'].split(' ')
		statusCode = int(status[1])
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

#Create all the required files	
def createFiles():
	global files, logFile, fetchedFile, unFectchedFile, goneFile, redirTempFile, redirPermFile, notModifedFile, duplicateFile, imageFile, mimeType
	logFile = open(statisticsPath + "/log", "w")
	unFectchedFile =  open(statisticsPath + "/unfetched", "w") #1
	fetchedFile =  open(statisticsPath + "/fetched", "w") #2
	goneFile = open(statisticsPath + "/gone", "w") #3
	redirTempFile = open(statisticsPath + "/redirTemp", "w") #4
	redirPermFile = open(statisticsPath + "/redirPerm", "w") #5
	notModifedFile = open(statisticsPath + "/notModified", "w") #6
	duplicateFile = open(statisticsPath + "/duplicate", "w") #7
	imageFile = open(statisticsPath + "/images", "w") #8
	files = [logFile,  unFectchedFile, fetchedFile, goneFile, redirTempFile, redirPermFile, notModifedFile, duplicateFile, imageFile]


#Create the output directory to store all the required files generated via this program with all permisions
def createStatsDir():
	print "Cleaning/Creating statistics directory"
	if not os.path.exists(statisticsPath):
		os.chmod(crawlFolder, 0777)
		os.makedirs(statisticsPath, 0777)
	else:
		os.chmod(crawlFolder, 0777)
		os.system("rm -rf " + statisticsPath + "/*")

#Wrapper for logs and filewriting
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
