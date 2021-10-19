#!/bin/bash
queryfile=$1
resultfile=$2
indexfile=$3
dictfile=$4

python query.py $1 $2 $4 $3
