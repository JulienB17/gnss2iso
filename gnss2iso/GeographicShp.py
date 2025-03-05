#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: julienbarneoud
"""
import os
import sys
sys.path.append('..')
import geopandas as gpd
import shapely.geometry as shpg
import logging
logging.getLogger().setLevel(logging.INFO)
import tqdm

#internal import
from gnss2iso.Station import Station

class GeographicShp:
    """
    Geographic tools:
        -find country code (3 chr)

    Based on shapefile data .shp
    
    Several methods available to find ISO code (see self.get_iso & self.get_att methods)
        * dist=True: based on distance btw Station & Polygon --> always iso code provided [default method]
        * buffer (float): station is not a point but a circle (centered on point) with Radius = buffer [unit depends on shapefile epsg: here 4326= degree] --> possibly country not found '000'. Default buffer=0 (i.e. no buffer)
        * else: basic station.point included on polygon --> countries not found '000' (most accurate according to shapefile data)
        
    """    
    def __init__(self, shapefile):
        """
        Parameters
        ----------
        shapefile : str
           shapefile path
        """
        self.shapefile = shapefile
        #build geopandas dataframe
        self.gdf = gpd.read_file(self.shapefile)
        self.shapefile_attr = list(self.gdf.columns)
        
        # Get minimum and maximum coordinates in shapefile
        # usefull to know lon & lat format (degree vs rad, (0,360) vs (-180,180)...)
        bounds = self.gdf.bounds
        lon_min = bounds['minx'].min()
        lat_min = bounds['miny'].min()
        lon_max = bounds['maxx'].max()
        lat_max = bounds['maxy'].max()
        
        self.sta_min = Station(lon=lon_min, lat=lat_min, name="sta_min")
        self.sta_max = Station(lon=lon_max, lat=lat_max, name="sta_max")
        self.shapefile_bbox = shpg.box(lon_min, lat_min, lon_max, lat_max)
        self.verbose_bbox = f"bbox: lon({self.sta_min.point.x},{self.sta_max.point.x}), lat:({self.sta_min.point.y},{self.sta_max.point.y})"
                
    
    ##############################################################################################################################
    ####    Check methods
    ##############################################################################################################################
    
    def check_geometries_validity(self):
        """
        Checks geometries in the shapefile: no intersection possible btw polygons

        """
        logging.info("Checking the validity of geometries in the shapefile ... ")
        valid = True
        
        # Fix invalid geometries
        self.gdf['geometry'] = self.gdf['geometry'].apply(lambda geom: geom.buffer(0) if not geom.is_valid else geom) #buffer 0 method

        for num, geom in enumerate(tqdm.tqdm(self.gdf.geometry)):
            
            try :
                if (geom.geom_type == 'Point') or (geom.is_empty) or not geom.is_valid:
                    logging.warning(f"'{(num, self.gdf.loc[num, 'NAME_LONG'])}' geometry: {geom.geom_type}")
                    pass
                else: #check intersection only if current geometry is a polygon
                    it = geom.intersection(self.gdf.geometry[num+1:])
                    
                    #get no empty
                    not_empty = it[~it.is_empty]
                    
                    #get no multilinestring
                    final_intersect = not_empty[not_empty.geom_type != 'MultiLineString']
                    final_intersect = final_intersect[final_intersect.geom_type != 'LineString']
                    final_intersect = final_intersect[final_intersect.geom_type != 'Point']
                    
                    
                    if final_intersect.shape[0] != 0:
                        logging.warning(f"Intersection btw '{(num, self.gdf.loc[num, 'NAME_LONG'])}' & {final_intersect}")
                        valid = False
            except Exception as e:
                logging.warning(f"{num} (type: {geom.geom_type}) exception: {e}")
                
        if valid:
            logging.info(" --> valid shapefile: no polygon intersection.\n")
            
                
        return valid
    
    
    def check_point(self, point):
        """
        Checks coordinates of a station point: sta is in shapefile bbox ?
        Ensures coordinates format: degree vs rad, lon: (0,360) vs (-180,180), etc.
        
        Parameters
        ----------
        point: shapely.geometry.Point obj
            Point object. It can be provided by Station.point attribute.
    
        Returns
        -------
        valid: bool
        """
        valid = self.shapefile_bbox.contains(point)
        
        if not valid:
            logging.warning(f"Station {point} not in shapefile {self.verbose_bbox}")
        return valid
    
    
    ##############################################################################################################################
    ####    get data from shapefile
    ##############################################################################################################################
          
    def get_attr(self, sta=None, lon=None, lat=None, point=None, attr=['ISO_A3_EH'], buffer=0, dist=True, get_dist=False):
        """
        Provides country attributes 'attr' for a station, from shapefile table.
                
        Possible input(s):
            -lon & lat (floats)
            or
            -sta (Station object, with sta.point attribute)
            or
            -point (shapely Point object)
            
        Several methods available to find ISO code (see self.get_iso & self.get_att methods)
            * dist=True: based on distance btw Station & Polygon --> always iso code provided [default method]
            * buffer (float): station is not a point but a circle (centered on point) with Radius = buffer [unit depends on shapefile epsg: here 4326= degree] --> possibly country not found '000'. Default buffer=0 (i.e. no buffer)
            * else: basic station.point included on polygon --> countries not found '000' (most accurate according to shapefile data)
            
        if dist & get_dist : return distance between station & shape with ISO code 
        WARNING : dist unit consistent with shapefile EPSG unit. Ex: epsg=4324 -> degree; epsg=4978 -> meter
                        
        Output(s):
            Attributs listed in 'attr'

        Parameters
        ----------
        sta : Station obj
            station object, with lon & lat attributes. Can be initialized with cartesian coordinates.
        lon : float
            longitude (same unit as in the shapefile)
        lat : float
            latitude (same unit as in the shapefile)
        point: shapely.geometry.Point obj
            Point object. It can be provided by Station.point attribute.
        attr : list of str, optional
            attribute(s) of interest in the shapefile (i.e. in self.gdf). The default is 'ISO_A3_EH'.
        buffer: float
            Add a distance buffer (degree unit) around station (1 degree <> 100 km). Default 0 (i.e. no buffer).
        dist: bool
            Select country with distance method: get country with min distance btw (point & polygon). distance=0 if point include
        get_dist: bool
            Return dist value in dataframe [WARNING : unit of shapefile. Ex: epsg=4324 -> degree unit; epsg=4978 -> meter unit]

        Returns
        -------
        pandas.dataframe with columns 'attr'

        """
        #create sta object
        if (not bool(point)) and (not bool(sta)): #sta & point object not provided by user, build it from 'lon' & 'lat' attribute
            sta = Station(lon=lon, lat=lat)
            
        if bool(sta):
            point = sta.point
            
               
        if not self.check_point(point) and not dist: #station not in shapefile bbox ? -> criteria not check if 'dist' method
            return None
        
        # add a buffer
        if bool(buffer):
            polygon = point.buffer(buffer)
        else: #no buffer
            polygon = point
                
        ## methods to find country
        
        if dist: #based on min dist
            dists = polygon.distance(self.gdf.geometry)
            idx_country = dists.idxmin()
            dist = dists[idx_country]
            
            #add dist column in df
            df_selected = self.gdf.loc[idx_country, attr]
            
            if get_dist:
                df_selected["dist"] = dist
            return df_selected
            
            
        else: #based on point intersection or inclusion
            idx_country = []
            for index, row in self.gdf.iterrows():
                if row['geometry'].intersects(polygon): #which country contains station, potentially with buffer
                    idx_country.append(index)
                
        if len(idx_country) == 0:
            logging.warning(f"No country found for sta '{point}'")
            return None #no data found
                
        else:
            if len(idx_country) > 1:
                logging.warning(f"Station {sta.point} in multiple countries/ polygons: '{idx_country}'.")
                
            return self.gdf.loc[idx_country, attr]
        
        
        
    def get_iso(self, sta=None, lon=None, lat=None, point=None, buffer=0, dist=True, get_dist=False):
        """
        Provides directly ISO 3 chr country code for station (lon, lat). This method apply: self.get_attr() with attr = [ISO_A3_EH]
        
        Possible input(s):
            -lon & lat (floats)
            or
            -sta (Station object, with sta.point attribute)
            or
            -point (shapely Point object)
            
        Several methods available to find ISO code (see self.get_iso & self.get_att methods)
            * dist=True: based on distance btw Station & Polygon --> always iso code provided [default method]
            * buffer (float): station is not a point but a circle (centered on point) with Radius = buffer [unit depends on shapefile epsg: here 4326= degree] --> possibly country not found '000'. Default buffer=0 (i.e. no buffer)
            * else: basic station.point included on polygon --> countries not found '000' (most accurate according to shapefile data)
            
        if dist & get_dist : return distance between station & shape with ISO code 
        WARNING : dist unit consistent with shapefile EPSG unit. Ex: epsg=4324 -> degree; epsg=4978 -> meter
            
        Output(s):
            Attributs listed in 'attr'

        Parameters
        ----------
        sta : Station obj
            station object, with lon & lat attributes. Can be initialized with cartesian coordinates.
        lon : float
            longitude (same unit as in the shapefile)
        lat : float
            latitude (same unit as in the shapefile)
        point: shapely.geometry.Point obj
            Point object. It can be provided by Station.point attribute.
        attr : list of str, optional
            attribute(s) of interest in the shapefile (i.e. in self.gdf). The default is 'ISO_A3_EH'.
        buffer: float
            Add a distance buffer (degree unit) around station (1 degree <> 100 km). Default 0 (i.e. no buffer)
        dist: bool
            Select country with distance method: get country with min distance btw (point & polygon). distance=0 if point include
        get_dist: bool
            Return dist value in dataframe [WARNING : dist unit consistent with shapefile EPSG unit. Ex: epsg=4324 -> degree; epsg=4978 -> meter]


        Returns
        -------
        iso: str (3 chr)
            if get_dist = True & dist=True: return a list with [iso,dist_value]
        """        
        iso = self.get_attr(lon=lon, lat=lat, sta=sta, point=point, attr=['ISO_A3_EH'], buffer=buffer, dist=dist, get_dist=get_dist)
        
        if type(iso) == type(None): #no country found
            iso = '000'
        else:
            iso = iso.values.reshape(-1) # [ 'FRA', dist]
            if not get_dist:
                iso = iso[0] #pnly code ISO 3chr
                        
        return iso
    
    
    def get_country_ISOdist(self, iso, sta=None, lon=None, lat=None, epsg="4978"):
        """ 
        Provides distance [m] between 'iso' country & sta.
        * distance in which epsg ? Default 4978 : WGS 84 [unit: meter]
        * In case of several polygon with 'ISO' code, get minimal distance
        * Unknown ISO code: dist=-1
        """
        #create sta object
        if not bool(sta): #sta & point object not provided by user, build it from 'lon' & 'lat' attribute
            sta = Station(lon=lon, lat=lat)
        
        #convert current gdf to dist [m]
        gdf_countries = self.gdf.to_crs(f'EPSG:{epsg}') # conversion latlon <> meter
        #ISO code possible in SOV or unit column
        #print("ISO", iso, ((iso not in gdf_countries["ISO_A3_EH"].values) and (iso not in gdf_countries["SOV_A3"].values)) , iso=="ZZZ")
        
        if ((iso not in gdf_countries["ISO_A3_EH"].values) and (iso not in gdf_countries["SOV_A3"].values)) or iso=="ZZZ": #unknown ISO code:
            dist = -1
        else:
            dist = sta.point_xyz.distance(gdf_countries.loc[(gdf_countries["ISO_A3_EH"]==iso) | (gdf_countries["SOV_A3"]==iso),"geometry"]).min() 
        return dist
        