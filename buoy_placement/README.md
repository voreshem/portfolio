# Buoy Placement!
## Cluster analysis on geolocation data
###### Using `KMeans` from `sklearn`

#### Usage:
*`buoy_placement` uses a GPX file from Strava,*
*to select buoy locations,*
*from a recorded kayaking session,*
*by using Cluster Analysis from scikit-learn,*
*to provide The Jupiter Inlet Foundation with locations,*
*for their conservation buoys.*

- **Ensure that `buoy_placement` _gpx_, _sh_, and _py_ files are together within the desired directory.**

- **Run _ALL_ actions with: `sh buoy_placement.sh`**
- **To only plot raw kayak session, run in bash: `$ python -c "import buoy_placement"`**
- **To only plot buoy locations, run in bash: `python buoy_placement.py`**

*The generated files are saved into the directory containing the __gpx__, __sh__, and __py__ files, from which the script was run.*
*In its final action, the script opens the newly-generated maps & text file, which contains the coordinates.*

### Files:
- `buoy_placement.sh`
    *Runs Python code & shell tasks for `buoy_placement`*
- `buoy_placement.py`
    *Python script that performs cluster analysis & geomapping on the data from `buoy_placement.gpx`
- `buoy_placement.gpx`
    *`Strava` session datafile*
- `buoy_placement_sites.png`
    *Map plot visualization, overlaying chosen buoy locations onto a satellite map tile*
- `buoy_placement_coordinates.txt`
    *Exported `.txt` file, containing the buoys' coordinates & average inter-buoy distance*
- `raw_map.png`
    *Map plot visualization, overlaying the raw `Strava` geolocation session data onto a satellite map tile*
- `buoy_difference.png`
    *Map plot visualization, with contrasting overlay of the raw `Strava` geolocation session data & the chosen buoy locations on a satellite map tile*

### Utilized:
- `Python 3.6`
    * `xmltodict`
    * `numpy`
    * `pandas`
    * `matplotlib`
    * `cartopy`
    * `geopy`
    * `sklearn`
- `ImageMagick`
    * `compare`
- `Strava`
- `Bash`
