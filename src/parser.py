import nutchpy
import re
node_path = "/Users/rahulagarwal/Desktop/GitProjects/MotherSpider/Nutch/nutch/segment/20150927195905/parse_data/part-00000/data"	
seq_reader = nutchpy.sequence_reader

total_documents = seq_reader.read(node_path)
image_documents = list()
for document in total_documents:
	ct = re.search('Content-Type=image',str(document))
	if ct is not None:
		image_documents.append(document)	
		print ct.group(0)






#print (seq_reader.head(1,node_path))
#print(seq_reader.slice(10,20,node_path))
