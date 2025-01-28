#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 12:25:34 2024

@author: julienbarneoud
"""

import numpy as np
import os


# GRS80 parameters
ae = 6378137.
fe = 0.00335281068118
ee = np.sqrt(2*fe - fe**2)
be = ae * np.sqrt(1 - ee**2)


#shapefile path
shapefile = '../data/ne_10m_admin_0_map_units/ne_10m_admin_0_map_units.shp'
NGL_DATABASE_PATH = '../database/NGL.db'

IGSR3_DATABASE_PATH = '../database/IGSR3.db'

## dict param names: consistent/ unique btw BDD table, DataHoldings, gps_sta
names_dataHolding = ['Sta','lat','lon', 'h', 'X', 'Y', 'Z', 'Dtbeg', 'Dtend','Dtmod','NumSol','StaOrigName']
names_gpsStaBdd = ['name', 'lat', 'lon', 'h_ellips', 'alt', 'date_begin', 'date_end', 'np', 'length', 'gaps']
names_era5 = ['CODE',    'lat',  'lon',  'alt',  'lat_gps',  'lon_gps',  'alt_gps',  'dist',  'delta_h']


## BDD names
names_Bdd_Station = ['code9chr', 'lat', 'lon', 'h_ellips','alt','X', 'Y', 'Z',
                     'date_begin', 'date_end', 'date_mod', 'date_lastupdate', 'np', 'length', 'gaps',
                     ]

names_Bdd_StationVersion_ = ['code9chr','version', 'year', 'code_ngl', 'date_begin', 'date_end', 'np', 'length', 'gaps']
names_Bdd_Era5Version_ = ['code_ngl', 'year', 'version', 'date_begin', 'date_end', 'np']

names_Bdd_Version = ['version',  'ref_dataholdings', 'date_begin', 'date_end', 'date_lastupdate']

names_Bdd_VersionProject_ = ['version', 'project']

names_Bdd_Project = ['project', 'date_begin', 'date_end']

# dict_dataH2bdd = {'Sta':'code', 'Lat(deg)':'lat(deg)', 'Long(deg)':'lon(deg)', 'Dtbeg':'datebegin', 'Dtend':'dateend','Dtmod':'datemod', 'NumSol': 'np'}
# dict_gpsSta2bdd = {'name':'code', 'lat':'lat(deg)', 'lon':'lon(deg)'}


###### path
root_ipsl = "../../../../.."
HOMEDATA_o = os.path.join(root_ipsl, 'homedata/bock')
SCRATCHX_o = os.path.join(root_ipsl, 'scratchx/bock')
PATH_list = "../data/list_download"
# Sample path template
#PATH_CRD_template = os.path.join(HOMEDATA_o, "$projet/0data/GPS/NGL/$version/")
