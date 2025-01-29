#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage for gnss2iso.Station class

@author: julienbarneoud
"""
from gnss2iso import Station
#######################################################################################
#Example usage
#######################################################################################

#init a station BRAZ
# init with geographic coordinates 
braz_360 = Station(lat=-15.9475, lon=312.1221, h=1106.0220, name='braz_360')    
#permissive lon format (-180, 180) or (0,360)
braz_180 = Station(lat=-15.9475, lon=312.1221-360, h=1106.0220, name='braz_180')
#init with its cartesian coordinates
braz_xyz = Station(x=4115014.0800, y=-4550641.5499, z=-1741444.0356, name='braz_xyz') #with geographic coordinates

print("Station objects:")
print("\nBRAZ from lat,lon(0,360) params:", braz_360.__dict__)
print("\nBRAZ from lat,lon(-180,180) params:", braz_180.__dict__)
print("\nBRAZ from xyz:", braz_xyz.__dict__)

        
