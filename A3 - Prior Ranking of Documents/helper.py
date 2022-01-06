import csv
import os
import json
from stemmer import PorterStemmer
import re
from collections import Counter
import math

stopwords = []

delims = [' ',",",".",":",";","'","\"","@","#","+","!","_","~","&","*","%","^","=","`","|","$","\n","(",")",">","<"]
def tokenize_string(string):
    for delim in delims:
        string = string.replace(delim," ")
    return string.split()

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
		if stemmed in stopwords or len(stemmed) < 3:
			continue
		if stemmed != '':
			output.append(stemmed)
		word = ''
	return output
    
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


def getTerms(collection_directory, doc):
	path = collection_directory+"/"+doc
	text = ""
	with open(path, encoding="utf8", errors = 'ignore') as file:
		text = file.read()
	words = tokenize_string(text)
	return stemming(words, stopwords)

def getJaccard(t1, t2):
	numerator = t1.intersection(t2)
	denominator = t1.union(t2)
	return len(numerator)/len(denominator)