#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global variables for this package

@author: julienbarneoud
"""

import numpy as np

# GRS80 parameters
ae = 6378137.
fe = 0.00335281068118
ee = np.sqrt(2*fe - fe**2)
be = ae * np.sqrt(1 - ee**2)
