#!/bin/bash

rm -Rf ./python3
python3 -m venv ./python3
./python3/bin/python3 -m pip install -r requirements.txt