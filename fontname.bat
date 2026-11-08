@echo off
@REM # -*- coding: utf-8; tab-width: 4; indent-tabs-mode: nil -*-

@REM
@REM fontname.py - as combined Batch/Python script
@REM Copyright (C) 2026 Matthias \"Maddes\" Bücher
@REM
@REM - this batch file creates and activates an appropriate Python Virtual Environment
@REM   in order to avoid messing up the system's Python environment
@REM - the Python script implements the program logic
@REM
@REM License: MIT License - https://spdx.org/licenses/MIT.html
@REM
@REM Project page: https://github.com/chrissimpkins/fontname.py
@REM

@REM Enable delayed expansion to process actual run time values in code blocks via exclamation mark
SETLOCAL EnableExtensions EnableDelayedExpansion

@cd /d "%~dp0"

@REM Use system default of python 3.x
SET PYTHON_VERSION=3
SET SCRIPT_NAME=%~n0
SET SCRIPT_DIR=%~dp0
SET SCRIPT_PY_NAME=%SCRIPT_NAME%.py

@REM Check for python and module venv
SET RC=0
py -%PYTHON_VERSION% -m venv -h >nul
SET RC=%ERRORLEVEL%
IF %RC% NEQ 0 (
  @echo ERROR: Python or module "venv" missing. Install from https://www.python.org/ 1>&2
  exit /b %RC%
)
SET RC=

@REM Check for virtual environment for python version
SET VENV_PATH=%SCRIPT_DIR%%SCRIPT_NAME%.venv-py%PYTHON_VERSION%
SET CREATE=0
IF NOT EXIST "%VENV_PATH%\" (
  SET CREATE=1
  @echo --- Initializing Python Virtual Environment at %VENV_PATH% 1>&2
  SET RC=0
  py -%PYTHON_VERSION% -m venv "%VENV_PATH%"
  SET RC=!ERRORLEVEL!
  if !RC! NEQ 0 (
    @echo ERROR: Failed to create virtual environment in %VENV_PATH%. 1>&2
    exit /b !RC!
  )
)
SET RC=

SET PYTHON_VERSION=
SET SCRIPT_NAME=
SET SCRIPT_DIR=

@REM Activate virtual environment
IF EXIST "%VENV_PATH%\bin\activate.bat" (
  call "%VENV_PATH%\bin\activate.bat"
) ELSE (
  IF EXIST "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
  ) ELSE (
    @echo ERROR: Unknown type of virtual environment in %VENV_PATH% 1>&2
    exit /b 1
  )
)

SET VENV_PATH=

@REM Check for additional python packages in virtual environment
IF %CREATE% NEQ 0 (
  python -m pip install --upgrade pip
)
@REM SPEEDUP: disable with 1 after virtual environment was created successfully the first time
SET DONT_CHECK=0
SET _CHECK=0
IF %DONT_CHECK% EQU 0 SET _CHECK=1
IF %CREATE% NEQ 0 SET _CHECK=1
@rem
SET "PYTHON_MODULES=fonttools;^>=4.0"
IF %_CHECK% NEQ 0 (
  SET i=1
  SET "CHECK_PYTHON_MODULE!i!=%PYTHON_MODULES: =" & set /A i+=1 & set "CHECK_PYTHON_MODULE!i!=%"
  for /F "tokens=1,* delims==" %%A in ('set CHECK_PYTHON_MODULE') DO (
    for /F "tokens=1-2 delims=;" %%C in ("%%B") DO (
      SET PYTHON_MODULE=%%C
      SET PYTHON_MODULE_VERSION=%%D
      @rem
      SET RC=0
      pip show -q "!PYTHON_MODULE!" 2>nul
      SET RC=!ERRORLEVEL!
      IF !RC! NEQ 0 (
        SET CREATE=1
        @echo --- Installing Python module !PYTHON_MODULE! !PYTHON_MODULE_VERSION! 1>&2
        SET RC=0
        pip install "!PYTHON_MODULE!!PYTHON_MODULE_VERSION!" 1>&2
        SET RC=!ERRORLEVEL!
        IF !RC! NEQ 0 (
          @echo ERROR: Failed 1>&2
          exit /b !RC!
        )
      )
    )
  )
  IF !CREATE! NEQ 0 @echo --- Initialization done 1>&2
)
SET RC=
SET PYTHON_MODULES=
SET _CHECK=
SET DONT_CHECK=

SET CREATE=

SET FONTNAME_PATH=%0
python "%SCRIPT_PY_NAME%" %*
SET FONTNAME_PATH=
