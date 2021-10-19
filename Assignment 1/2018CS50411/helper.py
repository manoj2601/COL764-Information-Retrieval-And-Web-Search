from bs4 import BeautifulSoup
import snappy
import sys
import os
from stemmer import PorterStemmer
import re

def lsb(a, b):
	bin = "{0:b}".format(a)
	return bin[-b:]

def encodec2(num):
	if(num==1):
		return "0"
	binString = "{0:b}".format(num)
	lx = len(binString)
	llx = len("{0:b}".format(lx))
	ullx = ""
	for i in range(0, llx-1):
		ullx += '1'
	ullx += '0'
	rett = ""
	rett += ullx
	rett += lsb(lx, llx-1)
	rett += lsb(num, lx-1)
	return rett

def encodec4(num):
	k = 6
	b = pow(2, k)
	q = (num-1)//b
	r = num-q*b-1
	cr = "{0:b}".format(r)
	while(len(cr) < 6):
		cr = "0"+cr
	ret = ""
	for i in range(0, q):
		ret += '1'
	ret += '0'
	ret += cr 
	return ret


def decodec4(word):
	j = 0
	v = []
	if (j == len(word)):
		return -1, -1
	cnt=0
	while (j < len(word) and word[j] != '0'):
		cnt+=1
		j+=1
	if j == len(word):
		return -1, -1
	j+=1
	q = cnt
	br = ""
	for i in range(0, 6):
		br += word[j]
		j+=1
	r = int(br, 2)
	x = r + q*64+1
	return x, j


def decodec2(word):
	j = 0
	v = []
	if(word[0] == '0'):
		return 1, 1
	if (j == len(word)):
		return -1, -1
	cnt=0
	while (j < len(word) and word[j] != '0'):
		cnt+=1
		j+=1
	if j == len(word):
		return -1, -1
	j+=1
	llx = cnt+1
	k = 0
	lx = int('1'+word[j:j+llx-1], 2)
	j = j+llx-1
	x = int('1'+word[j:j+lx-1], 2)
	return x, j+lx-1

def encodec1(num):
	ret = []
	binString = "{0:b}".format(num)
	while(len(binString)%7!=0):
		binString = '0'+binString
	word = ''
	j=0
	while(j<=len(binString)-8):
		word += binString[j]
		j+=1
		if(len(word) == 7):
			ret.append('1'+word)
			word = ''
	last = '0' + binString[-7:]
	ret.append(last)
	return ret

def decodec1(bytes):
	word = ""
	j = 0 
	ret = []
	while(j < len(bytes)):
		if(bytes[j][0] == '1'):
			word += bytes[j][1:]
		else:
			word += bytes[j][1:]
			ret.append(int(word, 2))
			word = ""
		j+=1
	return ret

def getPostingList2(l, word, fileHandlers):
	ret = []
	for (fname, length) in l:
		if(fname not in fileHandlers):
			fileHandlers[fname] = open(fname, 'rb')
		temp = 0
		while(4*temp < length):
			a = fileHandlers[fname].read(4)
			a = int.from_bytes(a, 'big')
			ret.append(a)
			temp+=1
	return ret

def stemming(line, stopwords):
	p = PorterStemmer()
	output = []
	for c in line:
		if c == '' or c in stopwords:
			continue
		word = c.strip()
		if word.isalpha():
			word = word.lower()
		stemmed = p.stem(word, 0, len(word)-1)
		stemmed = stemmed.strip()
		if stemmed in stopwords:
			continue
		if stemmed != '':
			output.append(stemmed)
		word = ''
	return output

def tokenization(line):
	return re.split(r'[,.:;"`\'\(\)\{\}\[\] ]+|\n', line)
	# return re.split(' |\n|\.|\,|\;|\:|\"|\(|\)|\{|\}|\[|\]|\'`', line)

def getDictIndexOLD(coll_path, stopwords, tags, xmlFiles):
	dict = {}
	indexFiles = []
	
	for file in xmlFiles:
		infile = open(coll_path+"/"+file, "r")
		contents = infile.read()
		contents = "<END>"+contents+"</END>"
		soup = BeautifulSoup(contents, 'xml')
		docs = soup.find_all('DOC')

		for doc in docs:
			lists = {}
			docname = doc.find('DOCNO').get_text().strip()
			docno = len(indexFiles)
			indexFiles.append(docname)
			str1 = ""
			for tag in tags:
				l = doc.find_all(tag)
				for ll in l:
					str1 += " "+ll.get_text()
			st = tokenization(str1)
			str1 = stemming(st, stopwords)
			
			s = set([])
			for ss in str1:
				s.add(ss)

			for ss in s:
				if ss in dict:
					dict[ss].append(docno)
				else:
					vec = []
					vec.append(docno)
					dict[ss] = vec
	return dict, indexFiles

def getDictIndex(coll_path, stopwords, tags, xmlFiles):
	dict = {} #temporary dict key: word, value: list of no.
	count = 0 #count in dict
	indexFiles = [] #docid to docno
	fileCount=0 #kitni files dump ho chuki h
	traking = {} #key: word, value: list of tuple(filename, length)
	
	for file in xmlFiles:
		infile = open(coll_path+"/"+file, "r")
		contents = infile.read()
		contents = "<END>"+contents+"</END>"
		soup = BeautifulSoup(contents, 'xml')
		docs = soup.find_all('DOC')

		for doc in docs:
			lists = {}
			docname = doc.find('DOCNO').get_text().strip()
			docno = len(indexFiles)
			indexFiles.append(docname)
			str1 = ""
			for tag in tags:
				l = doc.find_all(tag)
				for ll in l:
					str1 += " "+ll.get_text()
			st = tokenization(str1)
			str1 = stemming(st, stopwords)
			
			s = set([])
			for ss in str1:
				s.add(ss)

			for ss in s:
				count+=1
				if ss in dict:
					dict[ss].append(docno)
				else:
					vec = []
					vec.append(docno)
					dict[ss] = vec

				if(count == 1000000):
					fileName = "./dump/tempdict-"+str(fileCount)+".txt"
					newdict = open(fileName, "wb")
					start = 0
					for (key, val) in sorted(dict.items()):
						end = start + 4*(len(val))-1
						tt = (fileName, end-start+1)
						if key not in traking:
							v = []
							v.append(tt)
							traking[key] = v
						else:
							traking[key].append(tt)
						start = end+1
						for i in range(0, len(val)):
							newdict.write(val[i].to_bytes(4, byteorder = 'big'))
					count = 0
					fileCount+=1
					dict = {}
	if count != 0:
		fileName = "./dump/tempdict-"+str(fileCount)+".txt"
		newdict = open(fileName, "wb")
		start = 0
		for (key, val) in sorted(dict.items()):
			end = start + 4*(len(val))-1
			tt = (fileName, end-start+1)
			if key not in traking:
				v = []
				v.append(tt)
				traking[key] = v
			else:
				traking[key].append(tt)
			start = end+1
			for i in range(0, len(val)):
				newdict.write(val[i].to_bytes(4, byteorder = 'big'))
		count = 0
		fileCount+=1
		dict = {}
	return indexFiles, fileCount, traking


def changeBinaryc0(val):
	newlist = []
	newlist.append(val[0])
	for i in range(0, len(val)-1):
		newlist.append(val[i+1]-val[i])

	ret = []
	for i in range(0, len(newlist)):
		num = newlist[i]
		binString = "{0:032b}".format(num)
		ret.append(binString[0:8])
		ret.append(binString[8:16])
		ret.append(binString[16:24])
		ret.append(binString[24:32])
	return ret

def changeBinaryc1(val):
	newlist = []
	newlist.append(val[0])
	for i in range(0, len(val)-1):
		newlist.append(val[i+1]-val[i])
	ret = []
	for i in range(0, len(newlist)):
		num = newlist[i]
		s = encodec1(num)
		for i in range(0, len(s)):
			ret.append(s[i])
	return ret


def changeBinaryc2(val):
	newlist = []
	newlist.append(1+val[0])
	for i in range(0, len(val)-1):
		newlist.append(val[i+1]-val[i])

	ret = []
	prev = ""
	for i in range(0, len(newlist)):
		num = newlist[i]
		
		rett = prev
		rett += encodec2(num)
		j=0
		while(j+8 < len(rett)):
			ret.append(rett[j:j+8])
			j = j+8
		prev = rett[j:]
	if(len(prev) != 0):
		for i in range(0, 8-len(prev)):
			prev += '1'
		ret.append(prev)
	return ret


def changeBinaryc3(val):
	newlist = []
	newlist.append(val[0])
	for i in range(0, len(val)-1):
		newlist.append(val[i+1]-val[i])

	st = b''
	for i in range(0, len(newlist)):
		st += newlist[i].to_bytes(4, 'big')
	c = snappy.compress(st)
	return c


def changeBinaryc4(val):
	newlist = []
	newlist.append(1+val[0])
	for i in range(0, len(val)-1):
		newlist.append(val[i+1]-val[i])
	ret = []
	prev = ""
	for i in range(0, len(newlist)):
		num = newlist[i]
		
		rett = prev
		rett += encodec4(num)
		j=0
		while(j+8 < len(rett)):
			ret.append(rett[j:j+8])
			j = j+8
		prev = rett[j:]
	if(len(prev) != 0):
		for i in range(0, 8-len(prev)):
			prev += '1'
		ret.append(prev)
	return ret



def checkTraking(coll_path, stopwords, tags, xmlFiles, traking):
	#check if traking is correct
	dict, indexFiles2 = getDictIndexOLD(coll_path, stopwords, tags, xmlFiles)
	for (x, val) in dict.items():
		print(x)
		if val != getPostingList(traking, x):
			print("Impossible")
			exit(1)