#!/bin/sh

python_in=".."
python_out="../pyc"
python  pyc.py $python_in
cp -f  $python_in/*.pyc $python_out/
rm -rf $python_in/*.pyc