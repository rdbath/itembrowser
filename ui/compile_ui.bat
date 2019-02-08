@ECHO OFF

set OSGEO4W_ROOT=C:\OSGeo4W64

set PATH=%OSGEO4W_ROOT%\bin;%PATH%
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin

@echo off
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"
@echo off
path %OSGEO4W_ROOT%\apps\qgis-rel-dev\bin;%OSGEO4W_ROOT%\apps\grass\grass-7.4.4\lib;%OSGEO4W_ROOT%\apps\grass\grass-7.4.4\bin;%PATH%

cd /d %~dp0

@ECHO ON
::Ui Compilation
call pyuic5 ui_itembrowser.ui -o ui_itembrowser.py
call pyuic5 ui_settings.ui -o ui_settings.py          

::Resources
rem call pyrcc5 ui\resources.qrc -o gui\generated\resources_rc.py

@ECHO OFF
GOTO END

:ERROR
   echo "Failed!"
   set ERRORLEVEL=%ERRORLEVEL%
   pause

:END
@ECHO ON