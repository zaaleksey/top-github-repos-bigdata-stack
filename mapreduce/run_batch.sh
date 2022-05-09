#!/bin/bash
# shellcheck disable=SC2034
count_lines=$1

echo "Run 1: grouped"
head -n count_lines input/clicks.txt | python jobs/grouped.py -r local >output/grouped.txt
echo "Run 2: location"
python jobs/location.py -r local output/grouped.txt >output/location.txt
echo "Run 3: timestamp"
head -n count_lines input/clicks.txt | python jobs/timestamp.py -r local >output/time_location.txt
