#!/bin/bash

PRAC_TTL_ROOT_DIR=$1
VENDOR=$2
START_PRAC_NUM=$3
END_PRAC_NUM=$4

cd $PRAC_TTL_ROOT_DIR

for i in `seq $START_PRAC_NUM $END_PRAC_NUM`;
do
  echo "load zip file: ${VENDOR}_$i.zip ......"
  curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d "{}" "http://localhost:7200/rest/data/import/server/edr?fileName=${VENDOR}_$i.zip"
done
