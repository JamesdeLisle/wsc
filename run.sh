#!/bin/bash

#cd data/
#rm -R *
#cd ..
python main.py up
#python analysis.py
#python plot.py
find . -name "*.pyc" -type f -delete
find . -name "*~" -type f -delete
