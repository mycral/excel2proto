@echo off

set excel=%1
set python_cache=%2
set binary_cache=%3

echo "***********************************binary****************************************"
python  python\pyc\binary.pyc   %excel%    %python_cache%  %binary_cache%