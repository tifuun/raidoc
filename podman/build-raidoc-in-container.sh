#!/bin/sh

# This script runs inside the container.
# It makes a venv if it doesn't exist already,
# installs raimad and raidoc,
# and runs raidoc build

set -e

if ! [ -r venv/bin/python ]
then
	python -m venv venv
fi

. venv/bin/activate

if [ -n "$(ls venv/lib/python*/site-packages/raimad* )" ]
then
	echo "raimad installed, skipping " 2>&1
else
	echo "Installing raimad" 2>&1
	pip install raimad
fi

if [ -n "$(ls venv/lib/python*/site-packages/raidoc* )" ]
then
	echo "Raidoc installed, skipping " 2>&1
else
	echo "Installing raidoc in editable mode " 2>&1
	pip install -e .
fi

python -m raidoc build

set +e

