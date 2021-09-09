@echo off

set excel=%1
set classname_cache=%2
set cplusplus_mgr_cache=%3

echo "***********************************cplusplus********************************************"
python  python\pyc\cplusplus.pyc  %excel%  %classname_cache%  %cplusplus_mgr_cache%