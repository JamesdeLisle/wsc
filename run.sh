#!/bin/bash

#cd data/
#rm -R *
#cd ..
python main.py up
#python ctl/analysis.py
#python ctl/plot.py
find . -name "*.pyc" -type f -delete
find . -name "*~" -type f -delete
