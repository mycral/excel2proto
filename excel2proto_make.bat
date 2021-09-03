:: @echo off

set cur_path=%cd%

:: excel int path
set excel=%cur_path%\excel

:: go out path
set go_out=%cur_path%\..\..\example\excelconfig\config
set go_binary_out=%cur_path%\..\..\example\excelconfig\binary

:: csharp out path
set csharp_cfg_out=

::cplusplus out path
set cplusplus_out=

:: cache path 
set cache=%cur_path%\cache
set proto_cache=%cache%\proto
set python_cache=%cache%\python
set binary_cache=%cache%\binary
set classname_cache=%cache%\classname
set go_cache=%cache%\go_cfg
set go_mgr_cache=%cache%\go_cfg_mgr
set go_example=%cur_path%\python\example\go
set csharp_cache=%cache%\csharp_cfg
set csharp_mgr_cache=%cache%\csharp_cfg_mgr
set cplusplus_cache=%cache%\cplusplus_cfg
set cplusplus_mgr_cache=%cache%\cplusplus_cfg_mgr


python python\excel2proto.pyc %excel%  %proto_cache%  %python_cache% %classname_cache%\
protoc.exe  --proto_path %proto_cache% --python_out=%python_cache%  %proto_cache%\*.proto    
python  python\binary.pyc   %excel%\    %python_cache%\  %binary_cache%\  

if not %go_out% == "" (
    if not %go_binary_out% == "" (
        rmdir /s /q  %go_cache%
        mkdir %go_cache%
        protoc.exe  --plugin=protoc-gen-go=.\protoc-gen-go.exe  --proto_path %proto_cache%  --go_out %go_cache%   %proto_cache%\*.proto    
        
        python  python\go.pyc  %classname_cache%\  %go_mgr_cache%       
        xcopy  %go_cache%  %go_out%  /y
		xcopy  %go_example%    %go_out%  /y
        xcopy  %go_mgr_cache%  %go_out%  /y
        xcopy  %binary_cache%  %go_binary_out%  /y		
    )    
)
pause 

if not %cplusplus_out% == ""  (    
    protoc.exe  --proto_path %proto_cache% --cpp_out  %cplusplus_cache%  %proto_cache%\*.proto
    python  python\cplusplus_code.pyc  %binary_cache%    %cplusplus_mgr_cache%
    xcopy  %cplusplus_cache%  %cplusplus_out%  /y
    xcopy  %cplusplus_mgr_cache%  %cplusplus_out%  /y
)
pause 

if not %csharp_cfg_out% == ""  (
    protoc.exe  --proto_path %proto_cache% --csharp_out %csharp_cache%  %proto_cache%\*.proto
    python  python\csharp_code.pyc  %binary_cache%    %csharp_mgr_cache%
    xcopy  %csharp_cache%  %csharp_cfg_out%  /y
    xcopy  %csharp_mgr_cache%  %csharp_cfg_out%  /y
)
pause 
