I have used `python 3.6` to implement the program. Also, I have used the following imports:  

```
from bs4 import BeautifulSoup
import os
import json
import csv
import math
import re
import sys
from collections import Counter
```
   
The stemmer used here is same as assignment 1.   
### Commands to run the program:
./rocchio_rerank.sh <query_file.xml> <top_100_file.txt> <collection_file_directory> <output_file.txt>


The output will be stored in <output_file.txt>.

The directory structure:
There are 3 files of code:
1. `main.py` : This is the main file of the code
2. `helper.py` : Helper functions are implemented here
3. `stemmer.py` : Stemmer is implemented here

### Helper functions:
* `getRelevantDocuments(queryRel, i)`: It takes input an array of all queries and an index i and returns a list of all documents relevant to the (i+1)th query.
* `stemming(line, stopwords)`: It takes an array of strings (line) and an array of stopwords and returns an array of tokenized and stemmed array of words.
* `getQueries(filename)`: Extract the query part from the given xml file `filename` and returns a list of all queries.
* `tokenization(line)`: Tokenize the line.
* `getWords(path, metadata, id)`: Retrieve an array of words from the pmc or pdf json file of given cord id. Tokenize it, stem it and returns an array of words.
* `getTfIdf(allwords, text, lenDocs)`: For given text and total no. of documents, it returns an dictionary with TfIdf of each word for respective document.
* `getCosine(m1, m2)`: For given TfIdf vectors m1, m2, it returns the cosine value of both vectors.   
```
cosine(m1, m2) = (m1.m2)/(sqrt(m1)*sqrt(m2))
```