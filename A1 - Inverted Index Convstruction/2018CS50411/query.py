from bs4 import BeautifulSoup
from helper import stemming
from helper import tokenization
from helper import decodec2
from helper import decodec4
from helper import decodec1
import sys
from stemmer import PorterStemmer
import re
import snappy

if __name__ == '__main__':
	n = len(sys.argv)
	if n!= 5:
		print("less arguments")
		exit(1)
	queryFile = sys.argv[1]
	resultFile = sys.argv[2]
	dictFile = sys.argv[3]
	indexfile = sys.argv[4]

	dictfile = open(dictFile, 'r')
	binFile = open(indexfile, 'rb')
	queryfile = open(queryFile, 'r')
	resultfile = open(resultFile, 'w')

	cType = dictfile.readline().split()[0]

	dict = {}
	s = ''
	while True:
		s = dictfile.readline()
		s = s.split()
		if(s[0] == "!" and len(s) != 3):
			break
		if(len(s) != 3):
			exit(1)
		dict[s[0]] = (int(s[1]), int(s[2]))

	fileNames = []
	while True:
		s = dictfile.readline().split()
		if(len(s) == 0 or (s[0] == '!' and len(s) == 1)):
			break
		fileNames.append(s[0])

	stopwords = set([])
	s = dictfile.readline().split()
	for i in range(0, len(s)):
		stopwords.add(s[i])
	dictfile.close()


	if cType == "0":
		qno = 0
		while True:
			s = queryfile.readline()
			s = tokenization(s)
			s = stemming(s, [])
			if(len(s) == 0):
				break
			ret = []
			firstTime = True
			for word in s:
				l = []
				if word in dict:
					v = []
					s,e = dict[word]
					binFile.seek(s)
					j = s
					while(j < e+s):
						a = binFile.read(4)
						v.append(int.from_bytes(a, 'big'))
						j = j+4
					l = [v[0]]
					for i in range(0, len(v)-1):
						l.append(v[i+1]+l[i])
				else:
					if word in stopwords:
						continue
				if firstTime:
					ret = l
					firstTime = False
				else:
					ret = [value for value in l if value in ret]

			for i in range(0, len(ret)):
				resultfile.write("Q"+str(qno)+" ")
				resultfile.write(fileNames[ret[i]]+" ")
				resultfile.write("1.0\n")
			qno+=1
		resultfile.close()

	if cType == "1":
		qno = 0
		while True:
			s = queryfile.readline()
			s = tokenization(s)
			s = stemming(s, [])
			if(len(s) == 0):
				break

			ret = []
			firstTime = True
			for word in s:
				l = []
				if word in dict:
					v = []
					s,e = dict[word]
					binFile.seek(s)
					e = s+e
					j = s
					word = ""
					bytes = []
					while(j<=e):
						t = int.from_bytes(binFile.read(1), 'big')
						j+=1
						bytes.append("{0:08b}".format(t))
					v = decodec1(bytes)
					l = [v[0]]
					for i in range(0, len(v)-1):
						l.append(v[i+1]+l[i])
				else:
					if word in stopwords:
						continue
				if firstTime:
					ret = l
					firstTime = False
				else:
					ret = [value for value in l if value in ret]
			for i in range(0, len(ret)):
				resultfile.write("Q"+str(qno)+" ")
				resultfile.write(fileNames[ret[i]]+" ")
				resultfile.write("1.0\n")
			qno+=1
		resultfile.close()

	elif cType == "2":
		qno = 0
		while True:
			s = queryfile.readline()
			s = tokenization(s)
			s = stemming(s, [])
			if(len(s) == 0):
				break
			ret = []
			firstTime = True
			for wordd in s:
				l = []
				if wordd in dict:
					v = []
					s,e = dict[wordd]
					binFile.seek(s)
					e = s+e
					j = s
					word = ""
					while(j<=e):
						t = int.from_bytes(binFile.read(1), 'big')
						b = "{0:08b}".format(t)
						j+=1
						word += b

					j = 0
					v = []
					while j < len(word):
						x, y = decodec2(word[j:])
						if(x == -1 and y == -1):
							break
						j += y
						v.append(x)

					l = [v[0]-1]
					for i in range(0, len(v)-1):
						l.append(v[i+1]+l[i])
				else:
					if word in stopwords:
						continue	
				if firstTime:
					ret = l
					firstTime = False
				else:
					ret = [value for value in l if value in ret]
				
				
			for i in range(0, len(ret)):
				resultfile.write("Q"+str(qno)+" ")
				resultfile.write(fileNames[ret[i]]+" ")
				resultfile.write("1.0\n")
			qno+=1
		resultfile.close()

	elif cType == "3":
		qno = 0
		while True:
			s = queryfile.readline()
			s = tokenization(s)
			s = stemming(s, [])
			if(len(s) == 0):
				break
			ret = []
			firstTime = True
			for wordd in s:
				l = []
				if wordd in dict:
					v = []
					s,e = dict[wordd]
					binFile.seek(s)
					j = s
					word = ""
					t = binFile.read(e+1)
					a = snappy.decompress(t)					
					i =0
					while(i+4<=len(a)):
						v.append(int.from_bytes(a[i:i+4], 'big'))
						i = i+4

					l = [v[0]]
					for i in range(0, len(v)-1):
						l.append(v[i+1]+l[i])
				else:
					if word in stopwords:
						continue	
				if firstTime:
					ret = l
					firstTime = False
				else:
					ret = [value for value in l if value in ret]
				
			for i in range(0, len(ret)):
				resultfile.write("Q"+str(qno)+" ")
				resultfile.write(fileNames[ret[i]]+" ")
				resultfile.write("1.0\n")
			qno+=1
		resultfile.close()

	elif cType == "4":
		qno = 0
		while True:
			s = queryfile.readline()
			s = tokenization(s)
			s = stemming(s, [])
			if(len(s) == 0):
				break
			ret = []
			firstTime = True
			for wordd in s:
				l = []
				if wordd in dict:
					v = []
					s,e = dict[wordd]
					binFile.seek(s)
					e = s+e
					j = s
					word = ""
					while(j<=e):
						t = int.from_bytes(binFile.read(1), 'big')
						b = "{0:08b}".format(t)
						j+=1
						word += b

					j = 0
					v = []
					while j < len(word):
						x, y = decodec4(word[j:])
						if(x == -1 and y == -1):
							break
						j += y
						v.append(x)

					l = [v[0]-1]
					for i in range(0, len(v)-1):
						l.append(v[i+1]+l[i])
				else:
					if word in stopwords:
						continue	
				if firstTime:
					ret = l
					firstTime = False
				else:
					ret = [value for value in l if value in ret]
				
				
			for i in range(0, len(ret)):
				resultfile.write("Q"+str(qno)+" ")
				resultfile.write(fileNames[ret[i]]+" ")
				resultfile.write("1.0\n")
			qno+=1
		resultfile.close()