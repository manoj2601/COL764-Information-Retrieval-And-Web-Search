from bs4 import BeautifulSoup
from helper import getPostingList2
from helper import stemming
from helper import tokenization
from helper import getDictIndex
from helper import getDictIndexOLD
from helper import changeBinaryc0
from helper import changeBinaryc1
from helper import changeBinaryc2
from helper import changeBinaryc3
from helper import changeBinaryc4
from helper import checkTraking
import sys
import os
from stemmer import PorterStemmer
import re

if __name__ == '__main__':
	n = len(sys.argv)
	if(n != 6):
		print("Invalid arguments")
		exit(1)

	coll_path = sys.argv[1]
	indexfile = sys.argv[2]
	stopwordfile1 = sys.argv[3]
	stopwords = open(stopwordfile1, "r").read().split()
	
	compressionType = sys.argv[4]
	xml_tags_info = sys.argv[5]
	tags = open(xml_tags_info).read().split()[1:]
	xmlFiles = os.listdir(coll_path)
	

	indexFiles, fileCount, traking = getDictIndex(coll_path, stopwords, tags, xmlFiles)
	dictFile = open(indexfile+'.dict', 'w')
	dictFile.write(compressionType+"\n")
	binFile = open(indexfile+'.idx', 'wb')
	fileHandlers = {}
	if (compressionType == '0'):
		byteCount = 0
		for key, val in sorted(traking.items()):
			start = byteCount
			byts = changeBinaryc0(getPostingList2(val, key, fileHandlers))
			end = start+len(byts)-1
			byteCount = end+1
			dictFile.write(key+" ")
			dictFile.write(str(start)+" ")
			dictFile.write(str(end-start)+"\n")
			for j in range(0, len(byts)):
				binFile.write(int(byts[j], 2).to_bytes(1, byteorder = 'big'))

	elif(compressionType == '1'):
		byteCount = 0
		for key, val in sorted(traking.items()):
			start = byteCount
			byts = changeBinaryc1(getPostingList2(val, key, fileHandlers))
			end = start+len(byts)-1
			byteCount = end+1
			dictFile.write(key+" ")
			dictFile.write(str(start)+" ")
			dictFile.write(str(end-start)+"\n")
			for j in range(0, len(byts)):
				binFile.write(int(byts[j], 2).to_bytes(1, byteorder = 'big'))

	elif (compressionType == '2'):
		byteCount = 0
		# binFile.write(int('000', 2).to_bytes(1, byteorder = 'big'))
		for key, val in sorted(traking.items()):
			start = byteCount
			byts = changeBinaryc2(getPostingList2(val, key, fileHandlers))
			end = start + len(byts)-1
			byteCount = end+1
			dictFile.write(key+" ")
			dictFile.write(str(start)+" ")
			dictFile.write(str(end-start)+"\n")
			for j in range(0, len(byts)):
				binFile.write(int(byts[j], 2).to_bytes(1, byteorder = 'big'))
	
	elif(compressionType == '3'):
		#do something
		byteCount = 0 
		for key, val in sorted(traking.items()):
			start = byteCount
			byts = changeBinaryc3(getPostingList2(val, key, fileHandlers))
			end = start+len(byts)-1
			byteCount = end+1
			dictFile.write(key+" ")
			dictFile.write(str(start)+" ")
			dictFile.write(str(end-start)+"\n")
			binFile.write(byts)

	
	elif(compressionType == '4'):
		byteCount = 0
		# binFile.write(int('000', 2).to_bytes(1, byteorder = 'big'))
		for key, val in sorted(traking.items()):
			start = byteCount
			byts = changeBinaryc4(getPostingList2(val, key, fileHandlers))
			end = start + len(byts)-1
			byteCount = end+1
			dictFile.write(key+" ")
			dictFile.write(str(start)+" ")
			dictFile.write(str(end-start)+"\n")
			for j in range(0, len(byts)):
				binFile.write(int(byts[j], 2).to_bytes(1, byteorder = 'big'))

	elif(compressionType == '5'):
		#do something
		print("NOT IMPLEMENTED")

	for key, val in fileHandlers.items():
		val.close()
	dictFile.write('!\n')
	for i in range(0, len(indexFiles)):
		dictFile.write(indexFiles[i]+'\n')
	dictFile.write("!\n")
	for s in stopwords:
		dictFile.write(s+" ")
	dictFile.close()
	binFile.close()
