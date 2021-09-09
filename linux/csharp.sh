#!/bin/sh

classname_cache=$1
csharp_mgr_cache=$2

echo "***********************************csharp********************************************"
python  python/pyc/csharp.pyc  $classname_cache    $csharp_mgr_cache
