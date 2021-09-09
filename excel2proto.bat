@echo off

set cur_path=%cd%

:: excel int path
set excel=%cur_path%\excel

:: go out path
set go_out=%cur_path%\out\go_out
set go_binary_out=%cur_path%\out\go_binary_out

:: csharp out path
set csharp_out=%cur_path%\out\csharp_out
set csharp_binary_out=%cur_path%\out\csharp_binary_out

::cplusplus out path
set cplusplus_out=%cur_path%\out\cplusplus_out
set cplusplus_binary_out=%cur_path%\out\cplusplus_binary_out

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

call win\excel2proto.bat %excel%  %proto_cache%  %python_cache% %classname_cache%\
if not "%errorlevel%"=="0" (  
    pause  
    exit
)

call  win\binary.bat  %excel%\    %python_cache%\  %binary_cache%\
if not "%errorlevel%"=="0" (  
    pause
    exit
)

if not %go_out% == "" (
    if not %go_binary_out% == "" (
        rmdir /s /q  %go_cache%
        mkdir %go_cache%        
		protoc.exe  --plugin=protoc-gen-go=.\protoc-gen-go.exe --proto_path %proto_cache%  --go_out %go_cache%   %proto_cache%\*.proto
        call  win\go.bat %classname_cache%\  %go_mgr_cache%        
        if not "%errorlevel%"=="0" (
           pause
           exit
        )
        xcopy  %go_cache%  %go_out%  /y
		xcopy  %go_example%    %go_out%  /y
        xcopy  %go_mgr_cache%  %go_out%  /y
        xcopy  %binary_cache%  %go_binary_out%  /y
    )
)

if not %cplusplus_out% == "" (
    if not %cplusplus_binary_out% == "" (
        rmdir /s /q  %cplusplus_cache%
        mkdir %cplusplus_cache%
		protoc.exe  --proto_path %proto_cache% --cpp_out  %cplusplus_cache%  %proto_cache%\*.proto
		call  win\cplusplus.bat  %excel%\  %classname_cache%\  %cplusplus_mgr_cache%        
        if not "%errorlevel%"=="0" (
           pause
           exit
        )
		xcopy  %cplusplus_cache%  %cplusplus_out%  /y
		xcopy  %cplusplus_mgr_cache%  %cplusplus_out%  /y
		xcopy  %binary_cache%  %cplusplus_binary_out%  /y
    )
)

if not %csharp_out% == "" (
    if not %csharp_binary_out% == "" (
        rmdir /s /q  %csharp_cache%
        mkdir %csharp_cache%
		protoc.exe  --proto_path %proto_cache% --csharp_out %csharp_cache%  %proto_cache%\*.proto
		call  win\csharp.bat  %classname_cache%    %csharp_mgr_cache%   
        if not "%errorlevel%"=="0" (
           pause
           exit
        )                
		xcopy  %csharp_cache%  %csharp_out%  /y
		xcopy  %csharp_mgr_cache%  %csharp_out%  /y
		xcopy  %binary_cache%  %csharp_binary_out%  /y
    )
)   
pause 
