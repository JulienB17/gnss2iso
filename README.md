<h1 align="center" id="title">gnss2iso</h1>


Python toolbox for geographic &amp; geodetic data processing. **gnss2iso searches the ISO country code given the coordinates of a geodetic station.**

**Table of Contents**
1. [Installation](#installation)
    1. [Conda environment](#conda-env)
    1. [Install gnss2iso with pip](#pip-install)
1. [Project contain](#project)
    1. [GeographicShp](#geographic-class)
    1. [Station](#station-class)
1. [Data](#data)
1. [Example](#example)
1. [Developer's Corner](#dev)


<br/><br/>


<h2 id="installation">🛠️ Installation </h2>

- Clone this repository to your work space:

```
git clone https://github.com/JulienB17/gnss2iso.git
```

<h3 id="conda-env"> Conda environment </h3>

- To make the configuration easier, a conda environment is used: **gnss2iso_env.yml** env. This environments is exported as `.yml` file at the root */gnss2iso* of the repository. Ensure that **Conda** is installed on your computer. You can find the official documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

1. Create an environment from the `.yml` file: 
```
conda env create -f gnss2iso_env.yml
```
2. Check that the new environment **gnss2iso_env** is installed correctly:
```
conda env list
```
3. Activate the new conda environment :
```
conda activate gnss2iso_env
```
<h3 id="pip-install"> Install gnss2iso with <b><i> pip </b></i> </h3>

To install gnss2iso as a Python package, run at the root */gnss2iso*:
```
pip install [-e] .
```
> NOTE: -e option if for "editor" mode, this allows you to write code within gnss2iso without having to reinstall it after every change.

Now you can import gnss2iso in your python script !
```python
# import
from gnss2iso import Station, GeographicShp
```

<h2 id="project">📖 Project content</h2>

**Examples and simple use cases are provided in the** [examples folder](https://github.com/JulienB17/gnss2iso/tree/master/examples).


<h3 id="geographic-class"> 🗺️<b><i> GeographicShp </i> class </b></h3>

This class provides geographic tools, primarily for retrieving the **ISO country code** (from a .shp shapefile) for a specific geodetic station. It is built directly on [Station class](#station-class).

```
     Geographic tools:
        -find country code (3 chr)

    Based on shapefile data .shp
    
    Several options are available to search for an ISO code with get_iso() & get_att() methods:
        * if dist=True:    returns the ISO code of the nearest country, whatever the distance; it always returns an ISO code [default]
        * elseif buffer>0: returns the ISO code the nearest country within a circle centered on the station and with Radius = buffer [unit depends on shapefile epsg: degree or meter]
                           or '000' if no country is found within the circle
        * else:            returns the ISO code of the polygon containing the station
                           or '000' if no polygon is found

        if dist=TRUE & get_dist=TRUE: returns also the distance between station & polygon
   
```
> NOTE : You must have a geographic shapefile (.shp) to use GeographicShp. See the next section, [Data](#data).


<h3 id="station-class"> 🎯 <b><i> Station </i> class </b></h3>

This class creates a station object based on geographic or cartesian coordinates, providing attributes for position (longitude, latitude, height, and Cartesian components) and shapely point representations, along with methods to validate the station and convert coordinates between various systems.

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


<h2 id="data">📖 Data</h2>

Countries shapefiles can be found on [Natural Earth website.](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-details/).
Current dataset uses : 'units' divisions [downloadable here.](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_units.zip)

Download shapefile data on your local machine, for example inside a '/data' folder</p>

> NOTE: keep the entire folder downloaded from Natural Earth and do not move or delete files that seem useless! The . shp file has hidden dependencies with other . prj , etc. !

<h2 id="example"> ⚙️ Example </h2>

1. Import library
```python
# import
from gnss2iso import Station
from gnss2iso import GeographicShp
```

2. Build `GeographicShp`object using shapefile (see [Data section](#data)):
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
4. Get ISO code and attributes from shapefile
```python
iso = geo.get_iso(sta=sta, dist=True) #dist method: most efficient & less time consuming
print(f"{sta.name}: {iso}") #only ISO code as str

# dataframe with desired attibutes from shapefile table
iso_df = geo.get_attr(sta=abmf, attr=['NAME_LONG','ISO_A3_EH'],  get_dist=True) #ISO_A3_EH default used as ISO units code, get_dist get distance btw station & country shape
print(f"{abmf.name} ({abmf.lon}, {abmf.lat}) : '{iso_df['ISO_A3_EH']}' --> {iso_df['NAME_LONG']}; dist({abmf.name}-{iso_df['ISO_A3_EH']})={iso_df['dist']}")
```

```
#OUTPUT
ABMF: 'GLP' #iso code
ABMF (-61.528, 16.262): 'GLP' --> Guadeloupe; dist(ABMF-GLP)=0.0 #dist=0: station included in the country shape
```

5. Special attention: "units" vs "sovereignty/admin" ISO code

```python
iso_unit = geo.get_attr(sta=abmf, dist=True, attr=["ISO_A3_EH"]) #default based on units ISO code
iso_admin = geo.get_attr(sta=abmf, dist=True, attr=["ADM0_A3_US"])
print(f"ABMF: ISO units code '{iso_unit['ISO_A3_EH']}' ('Guadeloupe') vs. ISO admin code '{iso_admin['ADM0_A3_US']}' ('France')")
```

```
#OUTPUT
ABMF: ISO units code 'GLP' ('Guadeloupe') vs. ISO admin code 'FRA' ('France')
```

6. Possibility to get distance between ABMF station and any ISO country code (see GeographicShp.get\_country\_ISOdist() method):
```python
# see ISO list available in your shapefile (attribute geo.gdf["ISO_A3_EH"] or gdf_countries["SOV_A3"])
# distance to 'FRA' (France) country example
dist = geo.get_country_ISOdist("FRA", sta=abmf)
print(f"ABMF distance to FRA: {dist}m")
```
```
#OUTPUT
ABMF distance to FRA: 5014362.173544413m
```


<h2 id="dev">💻 Developer's Corner</h2>

As described in the previous sections [Project contain](#project), gnss2iso consists of **object-oriented Python scripts** with a list of methods and attributes.
Without necessarily going through a [pip installation](#pip-install), it is also possible to import the scripts directly into your projects and adapt them to your needs.

The same applies if you wish to add or modify certain methods to meet your specific requirements (e.g., a new method for assigning the ISO code or adapting field/attribute names to match your shapefiles instead of those from Natural Earth).

Technologies used in the project:
*   python

<h2> Contacts </h2>

* [Julien Barnéoud](https://www.ipgp.fr/annuaire/barneoud/)
