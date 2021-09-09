set python_in=".."
set python_out="..\pyc"
python  pyc.py %python_in%
xcopy  %python_in%\*.pyc  %python_out%\  /y		
del /f  /q %python_in%\*.pyc
pause 