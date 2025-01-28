<h1 align="center" id="title">geodpybox</h1>


<p id="description">Toolbox for geographic &amp; geodetic treatments</p>

**Table of Contents**
1. [Installation](#installation)
1. [Project architecture](#project)
    1. [Station](#ngl-module)
    1. [GeographicShp](#sitelog-module)
1. [Data](#data)


<br/><br/>


<h2 id="installation">🛠️ Installation </h2>

- Clone this repository to your desired place:

```
git clone https://github.com/JulienB17/geodpybox.git
```

- To make the configuration easier, a conda environment is used: **ngl** env. This environments is exported as `.yml` file at the root */ngl_tools* of the repository. Ensure that **Conda** is installed on your machine. You can find the official documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

1. Open a shell and go to setup files directory:
```
cd envs_setup
```
2. Then, to create an environment from the `.yml` file: 
```
conda env create -f ngl.yml
```
3. Verify that this new environment **ngl** is installed correctly:
```
conda env list
```
> NOTE: python libraries are listed in */envs_setup/requirements.txt*/
> NOTE: some tools required pytrf library



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

