@echo off
echo *******************************************************
echo * start %~f0
echo *******************************************************
echo.
echo *******************************************************
set "LAUNCH_DIR=%~dp0"
echo Launch_Directory : %LAUNCH_DIR%
echo *******************************************************
echo.
echo.
echo *******************************************************
set "CURRENT_DIR=%CD%"
echo Current_Directory : %CURRENT_DIR%
echo *******************************************************
echo.

echo *******************************************************
set "PYTHON_EXE_PATH=C:\Tools\Python\2.7.10\"
echo Python Executable Path : %PYTHON_EXE_PATH%
echo *******************************************************
echo.

echo *******************************************************
set "OUT_DIRECTORY_PATH=%CURRENT_DIR%\output"
echo OUT DIRECTORY PATH :%OUT_DIRECTORY_PATH%
echo *******************************************************
echo.

set /p "user_name=Enter PTC IMS User ID here (Ex : uidr2685):"
call :getPassword user_password "Enter PTC IMS User ID (uidxxxx) password here: "
:: The user's password has been stored in the variable %user_password%

::echo %user_name%
::echo %user_password%

%PYTHON_EXE_PATH%python.exe %CURRENT_DIR%\IMS_Url_FileDownload.py ims_url_download -H ims-adas -P 7001 -u %user_name% -p %user_password% -d %OUT_DIRECTORY_PATH%
if "%ERRORLEVEL%"=="0" (
    echo ===============================================
	echo **** Files from IMS Downloaded sucsessfully ***
	echo ===============================================
	echo.
	exit /b 0
) else (
  echo =================================================
  echo ***** Result: FAIL ******************************
  echo =================================================
  pause
  exit /b 1
)

::------------------------------------------------------------------------------
:: Masks user input and returns the input as a variable.
:: Password-masking code based on http://www.dostips.com/forum/viewtopic.php?p=33538#p33538
::
:: Arguments: %1 - the variable to store the password in
::            %2 - the prompt to display when receiving input
::------------------------------------------------------------------------------
:getPassword
set "_password="

:: We need a backspace to handle character removal
for /f %%a in ('"prompt;$H&for %%b in (0) do rem"') do set "BS=%%a"

:: Prompt the user 
set /p "=%~2" <nul 

:keyLoop
:: Retrieve a keypress
set "key="
for /f "delims=" %%a in ('xcopy /l /w "%~f0" "%~f0" 2^>nul') do if not defined key set "key=%%a"
set "key=%key:~-1%"

:: If No keypress (enter), then exit
:: If backspace, remove character from password and console
:: Otherwise, add a character to password and go ask for next one
if defined key (
    if "%key%"=="%BS%" (
        if defined _password (
            set "_password=%_password:~0,-1%"
            set /p "=!BS! !BS!"<nul
        )
    ) else (
        set "_password=%_password%%key%"
        set /p "="<nul
    )
    goto :keyLoop
)
echo/

:: Return password to caller
set "%~1=%_password%"
goto :eof

echo *
echo * end %~f0
echo *******************************************************

