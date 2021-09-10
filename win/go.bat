@echo off

set classname_cache=%1
set go_mgr_cache=%2


echo "***********************************go********************************************"
python  python\pyc\go.pyc  %classname_cache%  %go_mgr_cache% 