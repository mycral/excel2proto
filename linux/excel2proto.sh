#!/bin/sh

excel=$1
proto_cache=$2
python_cache=$3
classname_cache=$4

echo "***********************************excel2proto***********************************"
python python/pyc/excel2proto.pyc $excel  $proto_cache  $python_cache  $classname_cache
./protoc  --proto_path $proto_cache --python_out=$python_cache  $proto_cache/*.proto
