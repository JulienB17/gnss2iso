<h1 align="center" id="title">geodpybox</h1>


<p id="description">Toolbox for geographic &amp; geodetic treatments</p>

**Table of Contents**
1. [Installation](#installation)
1. [Project contain](#project)
    1. [Station](#station-class)
    1. [GeographicShp](#geographic-class)
1. [Data](#data)


<br/><br/>


<h2 id="installation">🛠️ Installation </h2>

- Clone this repository to your desired place:

```
git clone https://github.com/JulienB17/geodpybox.git
```

- To make the configuration easier, a conda environment is used: **geodpybox_env.yml** env. This environments is exported as `.yml` file at the root */geodpybox* of the repository. Ensure that **Conda** is installed on your machine. You can find the official documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

1. Create an environment from the `.yml` file: 
```
conda env create -f geodpybox_env.yml
```
2. Verify that this new environment **geodpybox_env** is installed correctly:
```
conda env list
```
3. If you want to install geodpybox as a Python package, run at the root */geodpybox*:
```
pip install . [-e]
```
> NOTE: -e option if for "editor" mode, if you plan on coding within geodpybox, so you won't have to reinstall after every change.

4. Now you can import geodpybox in your python script !
```python
# import
from geodpybox import Station, GeographicShp
```

<h2 id="project">📖 Project contain</h2>
Examples and simple use cases are provided in the `/examples` folder.

<h3 id="station-class"> 🎯 <b><i> Station </i> class </b></h3>

This class creates a station object based on geographic or cartesian coordinates, providing attributes for position (longitude, latitude, height, and Cartesian components) and shapely point representations, along with methods to validate the station and convert between coordinate systems.

```
    Build a station object from its coordinates (geographic or cartesian)
    
    
    Attributes:
        - lon      : longitudes [degree] (-180,180)
        - lon360   : longitudes [degree] (0,360)
        - lat      : latitudes [degree] (-90,90)
        - h        : height [m]
        - x        : cartesian x
        - y        : cartesian y
        - z        : cartesian z
        - point    : shapely point object from geographic coordinates
        - point_xyz: shapely point object from cartesian coordinates
        
    Methods:
        - valid_sta()
        - xyz2geo()
        - geo2xyz()
```


<h3 id="geographic-class"> 🗺️<b><i> GeographicShp </i> class </b></h3>

This class provides geographic tools, primarily for retrieving the ISO country code (from a .shp shapefile) for a specific geodetic station. It is built directly on the Station class.


```
     Geographic tools:
        -find country code (3 chr)

    Based on shapefile data .shp
    
    Several methods available to find ISO code (see self.get_iso & self.get_att methods)
        * dist=True: based on distance btw Station & Polygon --> always iso code provided
        * buffer=True: station is a circle with Radius = buffer [degree] --> countries not found '000'
        * default: station.point included on polygon --> countries not found '000' (most accurate according to shapefile data)
   
```
> NOTE : You must have a geographic shapefile (.shp) to use GeographicShp. See the next section, 'Data'.

<h2 id="data">📖 Data</h2>

Countries shapefile can be find on [Natural Earth website.](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-details/).
Current dataset used :'units' divisions [downloadable here.](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_units.zip)
<p>1. Download shapefile data on your local machine, inside */data* folder</p>

<p>2. For an easier usage, you can change & use string variable "shapefile" in *src.Global.shapefile*, with correct path to '.shp' file </p>

> NOTE: keep the entire folder downloaded from Natural Earth and do not move or delete files that seem useless! The . shp file has hidden dependencies with other . prj , etc. !


<h2>💻 Built with </h2>

Technologies used in the project:

*   python

<h2> Contacts </h2>

* [Julien Barnéoud](https://www.ipgp.fr/annuaire/barneoud/)
