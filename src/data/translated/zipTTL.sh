#!/bin/bash

PRAC_ROOT_DIR=$1
VENDOR=$2
START_PRAC_NUM=$3
END_PRAC_NUM=$4

cd $PRAC_ROOT_DIR

for i in `seq $START_PRAC_NUM $END_PRAC_NUM`;
do
  echo "zip files in $PRAC_ROOT_DIR/PRAC_$i/*.ttl ......: ${VENDOR}_$i.zip"
  zip -j ${VENDOR}_$i.zip $PRAC_ROOT_DIR/PRAC_$i/*.ttl
done
