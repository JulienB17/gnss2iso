#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage for gnss2iso.GeographicShp class

@author: julienbarneoud
"""
import os
from gnss2iso import Station
from gnss2iso import GeographicShp

#######################################################################################
#Example usage
#######################################################################################

file = "data/path/to/shp/file"
file = "data/ne_10m_admin_0_map_units/ne_10m_admin_0_map_units.shp"
if not os.path.isfile(file):
    raise ValueError(f"Geographic shapefile not found. Please check path '{file}' or download data (ex: https://www.naturalearthdata.com/downloads/10m-cultural-vectors/ -> 'Download map units')")
    
print("\n   ***   {}   ***  ".format(file.split("_")[-1]))

#Build Geographic obj from shapefile
geo = GeographicShp(file)
#access Shapfile attributes as geopandas dataframe
attr = geo.gdf
## check file geometries
## geo.check_geometries_validity() #time consuming, apply once 1st time you open your file

#stations (lon, lat) examples.
## We focus here on France and its ultra-marine territories (i.e. same administration/ sovereignty but not the same unit = different ISO country code)
paris = Station(2.33,48.8, name='PARIS')
cayenne = Station(-52.365, 4.822, name='CAYN')
reun = Station(55.572, -21.208, name='REUN')
abmf = Station(-61.528,16.262, name='ABMF')

#find sta countries ISO code in shapefile
for sta in [paris, cayenne, reun, abmf]:
    #directly iso 3 characters, '000' if no country found
    
    ##### several methods available to find ISO code
    # * dist=True: shortest distance btw Station & Polygon --> always return an ISO code [default]
    # * buffer (float): station is not a point but a circle (centered on point) with Radius = buffer [unit depends on shapefile epsg: here 4326= degree] --> possibly country not found '000'. Default buffer=0 (i.e. no buffer)
    # * otherswise: station must be included in Polygon --> possibly country not found '000' (most accurate according to shapefile data)
    
    #default dist=True: ISO get with min distance criteria (dist=0m -> point included in the country shape geometry)
    iso = geo.get_iso(sta=sta, dist=True) #dist method: most efficient & less time consuming
    print(f"{sta.name}: {iso}") #only ISO code as str
    # dataframe with desired attibutes from shapefile table
    iso_df = geo.get_attr(sta=sta, attr=['NAME_LONG','ISO_A3_EH'],  get_dist=True) #ISO_A3_EH default used as ISO units code, get_dist get distance btw station & country shape
    print(f"{sta.name} ({sta.lon}, {sta.lat}) : '{iso_df['ISO_A3_EH']}' --> {iso_df['NAME_LONG']}; dist({sta.name}-{iso_df['ISO_A3_EH']})={iso_df['dist']}")
    
    # sta: distance to 'FRA' (France) country example
    dist = geo.get_country_ISOdist("FRA", sta=sta)
    print(f"Distance to FRA: {dist}m")
        


###### special attention : "unit" vs "sovereignty/admin" ISO country code (ABMF example)
iso_unit = geo.get_attr(sta=abmf, dist=True, attr=["ISO_A3_EH"]) #default based on units ISO code
iso_admin = geo.get_attr(sta=abmf, dist=True, attr=["ADM0_A3_US"])
print(f"ABMF: ISO units code '{iso_unit['ISO_A3_EH']}' ('Guadeloupe') vs. ISO admin code '{iso_admin['ADM0_A3_US']}' ('France')")
