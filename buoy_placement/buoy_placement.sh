#---*--- Calculate Buoy Placement ---*---#
python -c "import buoy_placement"
python buoy_placement.py;
echo $'\nPlotting map difference!';
compare raw_map.png buoy_placement_sites.png buoy_difference.png;
echo $'\nDONE';
open *.png; open *.txt;