rem Execute script from Source Directory
CD > pwd.txt
set /p SRCD=<pwd.txt
set folder="C:\DIHMIGIT\dihmi"
cd /d %folder%
rem clean dst folder
if exist %folder% for /F "delims=" %%i in ('dir /b') do (rmdir "%%i" /s/q || del "%%i" /s/q)

if not exist %folder%\ MKDIR %folder%\
if not exist %folder%\SourceSpace\ MKDIR %folder%\SourceSpace\
if not exist %folder%\Tools\ MKDIR %folder%\Tools\

rem return to home
cd /d %SRCD%

rem excludes
set ex1=Infrastructure
set ex2=IntegrityBSP

rem link delispace
mklink /J %folder%\DeliSpace %SRCD%\DeliSpace

rem link sourceSpace
cd SourceSpace
FOR /F "delims==" %%d IN ('dir /a:d /b "%ROOT%"') DO (
    if %%d NEQ %ex1% mklink /J %folder%\SourceSpace\%%d %SRCD%\SourceSpace\%%d
)

rem link Tools
cd /d ../Tools
FOR /F "delims==" %%d IN ('dir /a:d /b "%ROOT%"') DO (
    if %%d NEQ %ex2% mklink /J %folder%\Tools\%%d %SRCD%\Tools\%%d
)
cd /d ../

copy %SRCD%\WorkspaceSettings.set %folder%\

rem cd /d %folder%

rem git add .
rem git commit -a -m "Update DI HMI repository."
rem git push origin master

rem cd /d %SRCD%