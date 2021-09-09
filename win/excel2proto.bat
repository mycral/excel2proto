@echo off

set excel=%1
set proto_cache=%2
set python_cache=%3
set classname_cache=%4

echo "***********************************excel2proto***********************************"
python python\pyc\excel2proto.pyc %excel%  %proto_cache%  %python_cache%  %classname_cache%
protoc.exe  --proto_path %proto_cache% --python_out=%python_cache%  %proto_cache%\*.proto