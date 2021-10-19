all:
	bash invidx.sh ./coll_path/ indexfilename stopwords.txt 1 xml_tags_info.txt

0:
	bash invidx.sh ./coll_path/ indexfilename0 stopwords.txt 0 xml_tags_info.txt

1:
	bash invidx.sh ./coll_path/ indexfilename1 stopwords.txt 1 xml_tags_info.txt

2:
	bash invidx.sh ./coll_path/ indexfilename2 stopwords.txt 2 xml_tags_info.txt

3:
	bash invidx.sh ./coll_path/ indexfilename3 stopwords.txt 3 xml_tags_info.txt

4:
	bash invidx.sh ./coll_path/ indexfilename4 stopwords.txt 4 xml_tags_info.txt

query0:
	bash boolsearch.sh queryFile.txt resultFile0.txt indexfilename0.idx indexfilename0.dict

query1:
	bash boolsearch.sh queryFile.txt resultFile1.txt indexfilename1.idx indexfilename1.dict

query2:
	bash boolsearch.sh queryFile.txt resultFile2.txt indexfilename2.idx indexfilename2.dict

query3:
	bash boolsearch.sh queryFile.txt resultFile3.txt indexfilename3.idx indexfilename3.dict

query4:
	bash boolsearch.sh queryFile.txt resultFile4.txt indexfilename4.idx indexfilename4.dict


clean:
	rm -rf dump/*
	rmdir dump
