from bs4 import BeautifulSoup
import csv
import os
import json
from stemmer import PorterStemmer
import re
from collections import Counter
import math


def getRelevantDocuments(queryRel, i):
	ret = []
	for j in range(0, len(queryRel[i])):
		ret.append(queryRel[i][j][2])
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

def getQueries(filename):
	with open(filename, 'r') as f:
		data = f.read()
	Bs_data = BeautifulSoup(data, 'xml')
	topics = Bs_data.find_all('topic')
	queryList = list(map(lambda x: x.find('query').get_text(), topics))
	return queryList

def tokenization(line):
	return re.split(r'[,.:;"`\'\(\)\{\}\[\] ]+|\n', line)
    
def getWords(path, metadata, id):
	t = metadata[id]
	pmc_json = t['pmc_json_files']
	pdf_json = t['pdf_json_files']
	if((not pmc_json == '') and os.path.exists((path+"/"+pmc_json))):
		st = path+"/"+pmc_json
		with open(st, 'r') as f:
			data = json.load(f)
	elif((not pdf_json == '') and os.path.exists(path+"/"+pdf_json)):
		with open(path+"/"+pdf_json, 'r') as f:
			data = json.load(f)
	else:
		# print("FILE does not exist neither in pdf nor in pmc")
		return []

	text = data['body_text'][0]['text']
	words = tokenization(text)
	return stemming(words, [])



def getTfIdf(allwords, text, lenDocs):
	words = tokenization(text)
	content = stemming(words, [])
	cnt = Counter(content)
	tf = {}
	for word in cnt:
		tf[word] = cnt[word]/len(content)
	idf = {}
	for word in cnt:
		idf[word] = math.log(lenDocs/allwords[word])

	tfIdf = {}
	for word in tf:
		tfIdf[word] = tf[word]*idf[word]
	return tfIdf


def getCosine(m1, m2):
	ret = 0
	sqrt1 = 0
	sqrt2 = 0
	for word in m1:
		if(word in m2):
			ret += m1[word]*m2[word]
	for word in m1:
		sqrt1 += m1[word]*m1[word]
	for word in m2:
		sqrt2 += m2[word]*m2[word]
	if(sqrt1 == 0):
		return 0
	if(sqrt2 == 0):
		return 0
	sqrt1 = math.sqrt(sqrt1)
	sqrt2 = math.sqrt(sqrt2)
	return ret/(sqrt1*sqrt2)