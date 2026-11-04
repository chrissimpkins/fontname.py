#!/bin/sh -eu
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: nil -*-

###
### fontname.py - as combined Shell/Python script
### Copyright (C) 2026 Matthias \"Maddes\" Bücher
###
### - this shell script creates and activates an appropriate Python Virtual Environment
###   in order to avoid messing up the system's Python environment
### - the Python script implements the program logic
###
### License: MIT License - https://spdx.org/licenses/MIT.html
###
### Project page: https://github.com/chrissimpkins/fontname.py
###

PYTHON_VERSION='3' ; ### Use system default of python 3.x
SCRIPT_NAME="$(basename "${0}")"
SCRIPT_DIR="$(dirname "${0}")"
SCRIPT_PY_NAME="${SCRIPT_NAME%.sh}.py"
SCRIPT_PY_PATH="${SCRIPT_DIR}/${SCRIPT_PY_NAME}"

### Determine python executable (Special case Windows)
unset -v PYTHON_EXE
if [ -n "${WINDIR:-}" ]; then
  PYTHON_EXE="py -${PYTHON_VERSION}"
else
  PYTHON_EXE="python${PYTHON_VERSION}"
fi

umask 0022

### Check for python module venv
RC=0 ; { ${PYTHON_EXE} -m venv -h >/dev/null ; } || RC="${?}"
if [ "${RC}" -ne 0 ]; then
  printf -- '%s\n' \
    'ERROR: Python module "venv" missing.' \
    "Either install via package manager, e.g. Debian/Ubuntu package \"python${PYTHON_VERSION}-venv\"" \
    "or via pip (Debian/Ubuntu package \"python${PYTHON_VERSION}-pip\" or https://packaging.python.org/en/latest/tutorials/installing-packages/ )." \
    1>&2
  return "${RC}" 2>/dev/null || exit "${RC}"
fi

### Check for virtual environment for python version
VENV_PATH="${SCRIPT_DIR}/${SCRIPT_PY_NAME%.py}.venv-py${PYTHON_VERSION}"
CREATE=''
if [ ! -d "${VENV_PATH}" ]; then
  CREATE='X'
  printf -- '%s\n' "--- Initializing Python Virtual Environment at ${VENV_PATH}" 1>&2
  RC=0 ; ${PYTHON_EXE} -m venv "${VENV_PATH}" || RC="${?}"
  if [ "${RC}" -ne 0 ]; then
    printf -- 'ERROR: %s\n' "Failed to create virtual environment in ${VENV_PATH}." 1>&2
    return "${RC}" 2>/dev/null || exit "${RC}"
  fi
fi

### Activate virtual environment
set +u ; ### workaround for older venv versions
if [ -s "${VENV_PATH}/bin/activate" ]; then
  . "${VENV_PATH}/bin/activate"
elif [ -s "${VENV_PATH}/Scripts/activate" ]; then
  . "${VENV_PATH}/Scripts/activate"
else
  printf -- 'ERROR: %s\n' "Unknown type of virtual environment in ${VENV_PATH}" 1>&2
  return 1 2>/dev/null || exit 1
fi
set -u

unset -v PYTHON_EXE PYTHON_VERSION RC SCRIPT_NAME SCRIPT_DIR SCRIPT_PY_NAME VENV_PATH

### Check for additional python packages in virtual environment
if [ -n "${CREATE}" ]; then
  python -m pip install --upgrade pip
fi
( ### sub-shell to protect original positional arguments
  DONT_CHECK='' ### SPEEDUP: disable with 'X' after the virtual environment was created successfully the first time
  if [ -z "${DONT_CHECK}" -o -n "${CREATE}" ];  then
    PYTHON_MODULES='fonttools'
    PYTHON_MODULES_VERSION='>=4.0'
    #
    set -- ${PYTHON_MODULES_VERSION}
    for PYTHON_MODULE in ${PYTHON_MODULES}
     do
      PYTHON_MODULE_VERSION="${1}"
      shift
      RC=0 ; { pip show -q "${PYTHON_MODULE}" 2>/dev/null ; } || RC="${?}"
      if [ "${RC}" -ne 0 ]; then
        CREATE='X'
        [ "${PYTHON_MODULE_VERSION}" != 'any' ] || PYTHON_MODULE_VERSION=''
        printf -- '%s\n' "--- Installing Python module ${PYTHON_MODULE}${PYTHON_MODULE_VERSION:+ ${PYTHON_MODULE_VERSION}}" 1>&2
        RC=0 ; { pip install "${PYTHON_MODULE}${PYTHON_MODULE_VERSION}" 1>&2 ; } || RC="${?}"
        if [ "${RC}" -ne 0 ]; then
          printf -- 'ERROR: %s\n' 'Failed.' 1>&2
          return "${RC}" 2>/dev/null || exit "${RC}"
        fi
      fi
    done
    [ -z "${CREATE}" ] || printf -- '--- Initialization done\n\n' 1>&2
  fi
)

unset -v CREATE

FONTNAME_PATH="${0}" "${SCRIPT_PY_PATH}" "${@}"
