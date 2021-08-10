#!/usr/bin/env bash

PYTHON_MIN_VER_MAJOR=3
PYTHON_MIN_VER_MINOR=8

PYTHON3_REF=$(which python3 | grep "/python3")
PYTHON_REF=$(which python | grep "/python")
GIT_ROOT=$(git rev-parse --show-toplevel)

VENV='venv'

error_msg() {
    echo "Requires Python version ${PYTHON_MIN_VER_MAJOR}.${PYTHON_MIN_VER_MINOR}+" >&2
}

python_ref() {
    local my_ref=$1
    echo $(${my_ref} -c \
        'import platform; major, minor, patch = platform.python_version_tuple(); print(major); print(minor);'
    )
}

check_version() {
    local major=$1
    local minor=$2
    local python_ref=$3
    if ! [[ ${major} -ge ${PYTHON_MIN_VER_MAJOR} && ${minor} -ge ${PYTHON_MIN_VER_MINOR} ]]; then
        error_msg
        exit 1
    fi
}

# Check versioning of python3 and python refs, in that order
for pyref in "${PYTHON3_REF}" "${PYTHON_REF}"; do
    if [[ ! -z ${pyref} ]]; then
        version=("$(python_ref ${pyref})")
        check_version ${version[0]} ${version[1]} ${pyref}
        python=${pyref}
        break
    fi
done
# Fail if python isn't installed
if [[ -z ${python} ]]; then
    error_msg
    exit 1
fi

cd ${GIT_ROOT} &>/dev/null
if ! [[ -d ${VENV} ]]; then
    ${python} -m venv ${VENV}
fi
source ${VENV}/bin/activate
if [[ -z ${VIRTUAL_ENV} ]]; then
    echo "Failed to source virtual env!" >&2
    exit 1
fi
pip3 install --upgrade pip -r requirements.txt
echo "Complete!"
