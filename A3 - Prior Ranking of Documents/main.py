from collections import Counter
from sknetwork.ranking import PageRank
import csv
import math
import re
import sys
import glob
from helper import getJaccard
from helper import getCosine
from helper import getTerms
from sknetwork.utils import edgelist2adjacency
type1 = sys.argv[1]
collection_directory = sys.argv[2]
output_file = sys.argv[3]

print(type1)
print(collection_directory)
print(output_file)
if(collection_directory[len(collection_directory)-1] == '/'):
	collection_directory = collection_directory[:-1]

docs = glob.glob(collection_directory+"/*/*")
docs = map(lambda x : x[len(collection_directory)+1:], docs)
docs = list(docs)

edge_list = []

if type1 == 'jaccard':
	termSet = {}
	for doc in docs:
		t = getTerms(collection_directory, doc)
		termSet[doc] = set(t)
	file = open(output_file, 'w')
	for i in range(0, len(docs)):
		for j in range(i+1, len(docs)):
			d1 = docs[i]
			d2 = docs[j]
			sim = getJaccard(termSet[d1], termSet[d2])
			if (sim <= 0.0000):
				continue
			edge_list.append((i, j, sim))
			file.write(d1+" "+d2+" "+str("{0:.4f}".format(sim))+"\n")
	file.close()

elif type1 == 'cosine':
	allwords = {}
	tfDocuments = {}
	total = {}
	for doc in docs:
		content = getTerms(collection_directory, doc)
		cnt = Counter(content)
		total[doc] = len(content)
		tfDocuments[doc] = cnt
		for word in cnt:
			if word not in allwords:
				allwords[word]=1
			else:
				allwords[word]+=1

	idf = {}
	for word in allwords:
		idf[word] = math.log2(1+(len(docs)/allwords[word]))

	tfIdfDocs = {}
	for doc in docs:
		cnt = tfDocuments[doc]
		tf = {}
		for word in cnt:
			tf[word] = 1 + math.log2(cnt[word])
		tfIdf = {}
		for word in tf:
			tfIdf[word] = tf[word]*idf[word]
		tfIdfDocs[doc] = tfIdf

	file = open(output_file, 'w')
	for i in range(0, len(docs)):
		for j in range(i+1, len(docs)):
			d1 = docs[i]
			d2 = docs[j]
			sim = getCosine(tfIdfDocs[d1], tfIdfDocs[d2])
			if (sim <= 0.0000):
				continue
			edge_list.append((i, j, sim))
			file.write(d1+" "+d2+" "+str("{0:.4f}".format(sim))+"\n")
	file.close()

graph = edgelist2adjacency(edge_list, undirected=True)
pageRank = PageRank()
rank = pageRank.fit_transform(graph)
print("total ranks: "+str(len(rank)))
print("total docs: "+str(len(docs)))
ret = []
for i in range(0, len(docs)):
	ret.append((docs[i], rank[i]))
file = open("pageranks_"+type1+".txt", 'w')

ret.sort(key = lambda item: -item[1])
for i in range(0, 20):
	file.write(ret[i][0]+" "+str(ret[i][1])+"\n")
file.close()