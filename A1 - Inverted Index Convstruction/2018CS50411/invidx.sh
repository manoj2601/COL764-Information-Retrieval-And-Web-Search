#!/bin/bash
coll_path=$1
indexfile=$2
stopwordfile=$3
t=$4
xml_tags_info=$5

mkdir dump
python invidx_cons.py $1 $2 $3 $4 $5
rm -rf dump/