import nutchpy
import sys
import commands 
import os
#./dump directory will have all the utput files

seg_path = sys.argv[1] 
node_path = sys.argv[2]

seq_reader = nutchpy.sequence_reader

os.system("mkdir ./dump")
fd1 = open("./dump/allContents", "w");
fd2 = open("./dump/allMetadata", "w");

content = seq_reader.read(seg_path)
metadata = seq_reader.read(node_path)

fd1.write(str(content))
fd2.write(str(metadata))

fd1.close()
fd2.close()

print "============Processing METADATA============"

failedURL = {}
successURL = []

fd3 = open("./dump/successURLS", "w")
fd4 = open("./dump/failedURLS", "w")

for entry in metadata:
    
    for field in entry:
        
        if "db_unfetched" in field:
            URL = str(entry[0]).split(',')[0] 
            byteOut = commands.getstatusoutput("./nutch parsechecker "+ str(URL))
            
            print byteOut[1] 

            failedURL[URL] = byteOut[1] 
            fd4.write(URL+":"+byteOut[1]+"\n\n")

        else:
            URL = str(entry[0]).split(',')[0] 
            successURL.append(URL)
            fd3.write(URL+"\n\n")


fd3.close()
fd4.close()



