@echo off

SET PRAC_TTL_ROOT_DIR=%1
SET VENDOR=%2
SET START_PRAC_NUM=%3
SET END_PRAC_NUM=%4

echo %PRAC_TTL_ROOT_DIR%
echo %VENDOR%
echo %START_PRAC_NUM%
echo %END_PRAC_NUM%

REM "No need to cd into the directory - graphdb workbench use default $home/graphdb_import/ dir for importing files. Or start graphdb with param: -Dgraphdb.workbench.importDirectory="E:/development/translated_data/""
REM cd %PRAC_TTL_ROOT_DIR%

SET CUR_PATH=%cd%

REM echo %CUR_PATH%

for /l %%a in (1,1,%END_PRAC_NUM%) do (
  echo "load zip file: %VENDOR%_%%a.zip ......"
  E:\development\curl-7.53.1\src\curl.exe -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d "{}" "http://localhost:7200/rest/data/import/server/edr?fileName=%VENDOR_%%a.zip"
)

REM downloaded curl executable from https://curl.haxx.se/download.html: Win64 x86_64 zip 	7.53.1 and unzipped to VM: E:\development\curl-7.53.1