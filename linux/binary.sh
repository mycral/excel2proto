#!/bin/sh


excel=$1
python_cache=$2
binary_cache=$3

echo "***********************************binary****************************************"
python  python/pyc/binary.pyc  $excel  $python_cache  $binary_cache

