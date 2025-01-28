#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: julienbarneoud
"""
import sys
sys.path.append('..')
import numpy as np
import shapely.geometry as shpg
import logging
logging.getLogger().setLevel(logging.INFO)

#internal import (earth parameters)
from geodpybox.Global import ae, fe, ee
   
class Station:
    
    """
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
    """
    
    def __init__(self, lon=None, lat=None, **kwargs):
        """
        Necessary arguments:
            -GEOGRAPHIC coordinates: 'lon', 'lat' (optional: 'h')
            or
            -CARTESIAN coordinates: 'x', 'y', 'z'
        
        Optional arguments: metadata, name..
        """
        ### init default attributes
         #cartesian coords
        self.lon = lon
        self.lat = lat
        self.h = 0
        
         #geographic coords
        self.x = None
        self.y = None
        self.z = None
        
        ## sta info
        self.name = "station1"
        self.iso = '000' #default: no country code
        
        ## updates with **kgwars
        self.__dict__.update(kwargs)
        
        # check station coordinate validity (enough coordinates provided)
        valid = self.valid_sta()
        if not valid:
            raise ValueError(f"Incorrect coordinates for Station obj :{self.__dict__ }. 'x' 'y' 'z' or 'lon', 'lat' must be specified.")
        
        if all(item is not None for item in [self.x, self.y, self.z]): #compute lon lat
            self.lon, self.lat, self.h = self.xyz2geo(self.x, self.y, self.z)
        else: #compute x, y, z coordinates
            self.x, self.y, self.z = self.geo2xyz(self.lon, self.lat, self.h)
        
        #lon180 & lon360
        lon180 = [self.lon-360 if self.lon > 180 else  self.lon][0] #lon360 (-180, 180)
        lon360 = [self.lon+360 if self.lon < 0 else self.lon][0] #lon360 (0,360)
        
        self.lon = lon180 #default longitude btw (-180,180)
        self.lon360 = lon360

        #build shapely point obj
        self.point = shpg.Point(self.lon, self.lat)
        self.point_xyz = shpg.Point(self.x, self.y, self.z)
        
    def valid_sta(self):
        """ Checks if enough inputs coordinates are provided """
        if all(item is not None for item in [self.lon, self.lat]) or all(item is not None for item in [self.x, self.y, self.z]):
            return True
        else:
            return False
        
        
    def xyz2geo(self, X, Y, Z):
        """
        Transform cartesian coordinates into geographical coordinates
        Based on GRS80 ellipsoid
        
        Parameters:
        -----------
            X, Y, Z: floats
                cartesian cordinates

        Returns
        -------
        lat : (...) array_like or float
            Latitude(s) [deg]
        lon : (...) array_like or float
            Longitude(s) [deg]. lon(-180, 180)
        h : (...) array_like or float
            Ellipsoidal height(s) [m]

        """
        p = np.sqrt(X**2 + Y**2)
        r = np.sqrt(X**2 + Y**2 + Z**2)
        u = np.arctan2(Z/p * (1 - fe + ee**2 * ae/r), 1)

        lon = 2 * np.arctan2(Y, X + p)
        lat = np.arctan2(Z * (1-fe) + ee**2 * ae * np.sin(u)**3, (1-fe) * (p - ee**2 * ae * np.cos(u)**3))
        h = p * np.cos(lat) + Z * np.sin(lat) - ae * np.sqrt(1 - ee**2 * np.sin(lat)**2)
        
        lat, lon = lat*180/np.pi, lon*180/np.pi #lon (-180,180)
        
        return lon, lat, h
                
    
    def geo2xyz(self, lon, lat, h=0):
        """
        Parameters
        ----------
        lon : float
            Longitude(s) [degree]
        lat : float
            Latitude(s) [degree]
        h : float
            Ellipsoidal height(s) [m]. Default: 0.
        """
        #rad conversion
        lon, lat = lon * np.pi/180, lat * np.pi/180
        
        N = ae / np.sqrt(1 - (ee*np.sin(lat))**2)
    
        X = (N + h) * np.cos(lat) * np.cos(lon)
        Y = (N + h) * np.cos(lat) * np.sin(lon)
        Z = (N*(1-ee**2) + h) * np.sin(lat)

        return X, Y, Z