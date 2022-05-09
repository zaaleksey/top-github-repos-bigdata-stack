#!/bin/bash
echo "Run 1: grouped"
python jobs/grouped.py -r local input/clicks.txt >output/grouped.txt
echo "Run 2: location"
python jobs/location.py -r local output/grouped.txt >output/location.txt
echo "Run 3: timestamp"
python jobs/timestamp.py -r local input/clicks.txt >output/time_location.txt
