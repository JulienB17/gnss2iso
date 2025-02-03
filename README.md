<h1 align="center" id="title">gnss2iso</h1>


Python toolbox for geographic &amp; geodetic treatments. **Provides the ISO country code for a geodetic station of interest.**

**Table of Contents**
1. [Installation](#installation)
    1. [Conda environment](#conda-env)
    1. [Install gnss2iso with pip](#pip-install)
1. [Project contain](#project)
    1. [GeographicShp](#geographic-class)
    1. [Station](#station-class)
1. [Example](#example)
1. [Data](#data)


<br/><br/>


<h2 id="installation">🛠️ Installation </h2>

- Clone this repository to your desired place:

```
git clone https://github.com/JulienB17/gnss2iso.git
```

<h3 id="conda-env"> Conda environment </h3>

- To make the configuration easier, a conda environment is used: **gnss2iso_env.yml** env. This environments is exported as `.yml` file at the root */gnss2iso* of the repository. Ensure that **Conda** is installed on your machine. You can find the official documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

1. Create an environment from the `.yml` file: 
```
conda env create -f gnss2iso_env.yml
```
2. Verify that this new environment **gnss2iso_env** is installed correctly:
```
conda env list
```
3. Activate your new conda environment :
```
conda activate gnss2iso_env
```
<h3 id="pip-install"> Install gnss2iso with <b><i> pip </b></i> </h3>

To install gnss2iso as a Python package, run at the root */gnss2iso*:
```
pip install [-e] .
```
> NOTE: -e option if for "editor" mode, if you plan on coding within gnss2iso, so you won't have to reinstall after every change.

Now you can import gnss2iso in your python script !
```python
# import
from gnss2iso import Station, GeographicShp
```

<h2 id="project">📖 Project contain</h2>

**Examples and simple use cases are provided in the** [examples folder](https://github.com/JulienB17/gnss2iso/tree/master/examples).


<h3 id="geographic-class"> 🗺️<b><i> GeographicShp </i> class </b></h3>

This class provides geographic tools, primarily for retrieving the **ISO country code** (from a .shp shapefile) for a specific geodetic station. It is built directly on [Station class](#station-class).

```
     Geographic tools:
        -find country code (3 chr)

    Based on shapefile data .shp
    
    Several methods available to find ISO code (see self.get_iso & self.get_att methods)
        * dist=True: based on distance btw Station & Polygon --> always iso code provided
        * buffer=True: station is a circle with Radius = buffer [degree] --> countries not found '000'
        * default: station.point included on polygon --> countries not found '000' (most accurate according to shapefile data)
   
```
> NOTE : You must have a geographic shapefile (.shp) to use GeographicShp. See the next section, [Data](#data).


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

<h2 id="example"> ⚙️ Example </h2>

1. Import library
```python
# import
from gnss2iso import Station
from gnss2iso import GeographicShp
```

2. Build `GeographicShp`object using shapefile:
```python
#path to shapefile
file = "data/ne_10m_admin_0_map_units/ne_10m_admin_0_map_units.shp"
#Build Geographic obj from shapefile
geo = GeographicShp(file)
#access Shapfile attributes as geopandas dataframe
attr = geo.gdf
```

3. Create a `Station` of interest (example of [ABMF IGS station](https://webigs-rf.ign.fr/stations/ABMF)) :
```python
abmf = Station(-61.528,16.262, name='ABMF')
```
4. Get ISO from shapefile :
```python
iso = geo.get_iso(sta=sta, dist=True, get_dist=True) #dist method: most efficient & less time consuming
print(f"{sta.name}: {iso}") #only ISO code as str

# dataframe with desired attibutes from shapefile table
iso_df = geo.get_attr(sta=sta, attr=['NAME_LONG','ISO_A3_EH']) #ISO_A3_EH default used as ISO units code
print(f"{sta.name} ({sta.lon}, {sta.lat}) : '{iso_df['ISO_A3_EH']}' --> {iso_df['NAME_LONG']}")
```

```
#OUTPUT
ABMF: ['GLP' 0.0] #iso code + dist=0.0: station included in the country shape
ABMF (-61.528, 16.262) : 'GLP' --> Guadeloupe
```

5. Special attention : "units" vs "sovereignty/admin" ISO country code

```python
iso_unit_abmf = geo.get_attr(sta=abmf, dist=True, attr=["ISO_A3_EH"]) #default based on units ISO code
iso_admin_abmf = geo.get_attr(sta=sta, dist=True, attr=["ADM0_A3_US"])
print(f"ABMF station: ISO units code '{iso_unit_abmf['ISO_A3_EH']}' ('Guadeloupe') vs. ISO admin country code '{iso_admin_abmf['ADM0_A3_US']}' ('France')")
```

```
#OUTPUT
ABMF station: ISO units code 'GLP' ('Guadloupe') vs. ISO admin country code 'FRA' ('France')
```


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
