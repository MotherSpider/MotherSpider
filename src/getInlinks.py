#!/usr/bin/python
"""generate inlinks on your individual crawled data segments using the following command:

bin/nutch readlinkdb <linkdb> (-dump <out_dir> | -url <url>)
eg: bin/nutch readlinkdb crawl/linkdb -dump myoutput/out1

and then on the generated "part-xxxx", run this script as follows:

./getInlinks <path to generated file>
"""

import os
import sys

outlinkFile = open(sys.argv[1], "r");
os.makedirs("allInlinks");

content = outlinkFile.read()
recordList = content.split("\n\n");
count = 1

print len(recordList)
for rec in recordList:
    linkCount = 0
    linkList = []
    if "Inlinks:" in rec:
        tempRec = rec.split("\n");
        mainURL = rec.split()[0]
        for line in tempRec:
            if "fromUrl:" in line:
                linkList.append(line.lstrip("fromUrl:").split()[1])
        if (len(mainURL) != 0 and len(linkList) != 0):
            writefile = open("allInlinks/"+str(count)+".txt", "w")
            for url in linkList:
                writefile.write(mainURL+" "+url+"\n");
	    writefile.close()            
    count = count+1 
        

        
        
        
