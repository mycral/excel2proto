#!/bin/sh

cur_path=`pwd`

#excel int path
excel=$cur_path/excel

#go out path
go_out=$cur_path/out/go_out
go_binary_out=$cur_path/out/go_binary_out

#csharp out path
csharp_out=$cur_path/out/csharp_out
csharp_binary_out=$cur_path/out/csharp_binary_out

#cplusplus out path
cplusplus_out=$cur_path/out/cplusplus_out
cplusplus_binary_out=$cur_path/out/cplusplus_binary_out

#cache path 
cache=$cur_path/cache

proto_cache=$cache/proto
python_cache=$cache/python
binary_cache=$cache/binary
classname_cache=$cache/classname
go_cache=$cache/go_cfg
go_mgr_cache=$cache/go_cfg_mgr
go_example=$cur_path/python/example/go
csharp_cache=$cache/csharp_cfg
csharp_mgr_cache=$cache/csharp_cfg_mgr
cplusplus_cache=$cache/cplusplus_cfg
cplusplus_mgr_cache=$cache/cplusplus_cfg_mgr

./linux/excel2proto.sh  $excel  $proto_cache  $python_cache $classname_cache/
if [ $? != 0 ]; then
    exit
fi 

./linux/binary.sh  $excel    $python_cache $binary_cache/
if [ $? != 0 ]; then
    exit
fi

if [ $go_out != "" ]; then
    if [ $go_binary_out != "" ]; then    
        rm -rf  $go_cache
        mkdir -p $go_cache
        protoc  --plugin=protoc-gen-go=./protoc-gen-go  --proto_path $proto_cache  --go_out $go_cache   $proto_cache/*.proto
        ./linux/go.sh  $classname_cache  $go_mgr_cache   
        if [ $? != 0 ]; then
          exit
        fi     
        cp   $go_cache/*    $go_out  
		cp   $go_example/*    $go_out  
        cp   $go_mgr_cache/*  $go_out  
        cp   $binary_cache/*  $go_binary_out  
    fi 
fi 

if [ $cplusplus_out != "" ]; then
    if [ $cplusplus_binary_out != "" ]; then    
        rm -rf  $cplusplus_cache
        mkdir -p $cplusplus_cache
		protoc  --proto_path $proto_cache --cpp_out  $cplusplus_cache  $proto_cache/*.proto
        ./linux/cplusplus.sh  $excel   $classname_cache    $cplusplus_mgr_cache	
        if [ $? != 0 ]; then
          exit
        fi     	
		cp   $cplusplus_cache/*  $cplusplus_out  
		cp   $cplusplus_mgr_cache/*  $cplusplus_out  
		cp   $binary_cache/*  $cplusplus_binary_out 
    fi
fi

if [ $csharp_out != "" ]; then
    if [ $csharp_binary_out != "" ]; then    
        rm -rf  $csharp_cache
        mkdir -p $csharp_cache
		protoc  --proto_path $proto_cache --csharp_out $csharp_cache  $proto_cache/*.proto
        ./linux/csharp.sh  $classname_cache    $csharp_mgr_cache
        if [ $? != 0 ]; then
          exit
        fi     
		cp   $csharp_cache/*  $csharp_out  
		cp   $csharp_mgr_cache/*  $csharp_out  
		cp   $binary_cache/*  $csharp_binary_out  
    fi
fi