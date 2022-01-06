from collections import Counter
import csv
import math
import re
import sys
from helper import getWords
from helper import getQueries
from helper import getTfIdf
from helper import getRelevantDocuments
from helper import getCosine

query_file = sys.argv[1]
top_100_file = sys.argv[2]
collection_file = sys.argv[3]
output_file = sys.argv[4]

queryList = getQueries(query_file)
file = open(collection_file+'/metadata.csv')
csvreader = csv.reader(file)
header = next(csvreader)
metadata = {}
j = 0
for row in csvreader:
	j+=1
	dict = {}
	for i in range(0, len(header)):
		content = row[i].split("; ")
		dict[header[i]] = content[0]
		metadata[row[0]] = dict

	
file.close()
file = open(top_100_file, 'r')
queryRel = []


#filling queryRel
for i in range(0, 40):
	temp = []
	for j in range(0, 100):
		line = file.readline()
		words = re.split(' ', line)
		temp.append(words)
	queryRel.append(temp)

file.close()
docs = []
i=0
for key in metadata:
	docs.append(key)
	i+=1
	if i==100000:
		break
docs = set(docs)

for i in range(0, 40):
	for j in range(0, 100):
		docs.add(queryRel[i][j][2])

allwords = {}
tfDocuments = {}
total = {}
for doc in docs:
	content = getWords(collection_file, metadata, doc)
	cnt = Counter(content)
	total[doc] = len(content)
	tfDocuments[doc] = cnt
	for word in cnt:
		if word not in allwords:
			allwords[word] = 1
		else:
			allwords[word] += 1	


tfIdfDocs = {}
for doc in docs:
	cnt = tfDocuments[doc]
	tf = {}
	for word in cnt:
		tf[word] = cnt[word]/total[doc]
	
	idf = {}
	for word in cnt:
		idf[word] = math.log(len(docs)/allwords[word])
	tfIdf = {}
	for word in tf:
		tfIdf[word] = tf[word]*idf[word]
	tfIdfDocs[doc] = tfIdf


#got tfIdf of each document in vector form
#find tfIdf of queries
tfIdfQueries = {}
for i in range(0, len(queryList)):
	tfIdfQueries[queryList[i]] = getTfIdf(allwords, queryList[i], len(docs))



alpha = 1
beta = 0.7
gamma = 0.1
#Rocchio Method of Relevance Feedback
newTfIdf = {}
for i in range(0, len(queryList)):
	Dr = getRelevantDocuments(queryRel, i)
	avgDr = {}
	size = len(Dr)
	for word in allwords:
		sum = 0
		for d in Dr:
			if(word in tfIdfDocs[d]):
				sum += tfIdfDocs[d][word]
		avgDr[word] = (sum/size)*beta
	
	size = len(docs)-size
	avgDn = {}
	for word in allwords:
		sum = 0
		for doc in docs:
			if doc in Dr:
				continue
			if word in tfIdfDocs[doc]:
				sum += tfIdfDocs[doc][word]
		avgDn[word] = (sum/size)*gamma
	newTfIdf1 = {}
	for word in allwords:
		newTfIdf1[word] = 0
		if word in tfIdfQueries[queryList[i]]:
			newTfIdf1[word] += alpha*tfIdfQueries[queryList[i]][word]
		if word in avgDr:	
			newTfIdf1[word] +=avgDr[word]
		if word in avgDn:
			newTfIdf1[word] -= avgDn[word]
	newTfIdf[queryList[i]] = newTfIdf1


def compare(item1):
	return item1[0]

#new modified tf Idf of queries created 
file = open(output_file, 'w')
for i in range(0, len(queryList)):
	newCosines = {}
	Dr = getRelevantDocuments(queryRel, i)
	for doc in Dr:
		newCosines[doc] = getCosine(newTfIdf[queryList[i]], tfIdfDocs[doc])
	l = []
	for doc in newCosines:
		l.append((newCosines[doc], doc))
	l.sort(key = lambda x: x[0])
	for j in range(0, len(l)):
		file.write(str(i+1)+" Q0 "+str(l[len(l)-1-j][0])+" "+str(j+1)+" "+str(l[len(l)-1-j][1])+" runid1")
file.close()