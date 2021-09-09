#!/bin/sh

cur_path=`pwd`
	
rm -rf $cur_path/cache
rm -rf $cur_path/out/go_out/*
rm -rf $cur_path/out/go_binary_out/*
rm -rf $cur_path/out/csharp_out/*
rm -rf $cur_path/out/csharp_binary_out/*
rm -rf $cur_path/out/cplusplus_out/*
rm -rf $cur_path/out/cplusplus_binary_out/*
echo "clear cache out ok ..."
