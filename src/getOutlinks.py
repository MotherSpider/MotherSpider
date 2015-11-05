#!/usr/bin/python
"""generate outlinks on your individual crawled data segments using the following command:

bin/nutch readseg -dump crawl/segments/20110919084424/ outputdir2 -nocontent -nofetch - nogenerate -noparse -noparsetext

and then on the generated "dump", run this script as follows:

./getAllOutlinks <path to dump file>
"""

import os
import sys

outlinkFile = open(sys.argv[1], "r");
os.makedirs("allOutlinks");

content = outlinkFile.read()
recordList = content.split("Recno::");
count = 1

print len(recordList)
for rec in recordList:
    linkCount = 0
    linkList = []
    if "Outlinks:" in rec:
        tempRec = rec.split("\n");
        for line in tempRec:
            if "URL::" in line:
                mainURL = line.split()[1]
            if "toUrl:" in line:
                linkList.append(line.lstrip("outlink: toUrl:").split()[0])
        if (len(mainURL) != 0 and len(linkList) != 0):
            writefile = open("allOutlinks/"+str(count)+".txt", "w")
            for url in linkList:
                writefile.write(mainURL+" "+url+"\n");
	    writefile.close()            
    count = count+1 
        

        
        
        
