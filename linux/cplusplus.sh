#!/bin/sh

excel=$1
classname_cache=$2
cplusplus_mgr_cache=$3

echo "***********************************cplusplus********************************************"
python  python/pyc/cplusplus.pyc  $excel   $classname_cache    $cplusplus_mgr_cache
