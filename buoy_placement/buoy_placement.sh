#!/bin/bash
# Runs Python code & shell tasks for buoy_placement.

#---*--- Calculate Buoy Placement ---*---#

clear;

echo $'\nPlotting map of raw data!';
python -c "import buoy_placement";
echo $'Raw data FINISHED!';

echo $'\nPlotting buoy locations!';
python buoy_placement.py;
echo $'Buoy locations FINISHED!';

echo $'\nPlotting map difference!';
compare raw_map.png buoy_placement_sites.png buoy_difference.png;
echo $'Map difference FINISHED!';

echo $'\nOpening files!';
open *.png; open *.txt;

echo $'\n\nALL DONE!\n';
