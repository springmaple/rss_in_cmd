@ECHO OFF
SET CWD=%cd%
CD /D %~dp0\scripts
python %1.py %2 %3
CD /D %CWD%
