#!/bin/bash

cd data/
rm -R *
cd ..
python main.py
python analysis.py
python plot.py
