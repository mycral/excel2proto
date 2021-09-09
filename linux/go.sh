#!/bin/sh

classname_cache=$1
go_mgr_cache=$2

echo "***********************************go********************************************"
python  python/pyc/go.pyc  $classname_cache  $go_mgr_cache
