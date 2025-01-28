#!/bin/bash

python3 src/main.py
cd public && python3 http.server 8888
