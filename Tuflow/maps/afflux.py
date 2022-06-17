"""
Author: Tom Norman 
Licence GPL3
Description:
script to produce flood afflux maps from existing scenario (base) and design scenario.
Base a design rasters must have the same crs and extent. 
"""

from numpy import less
import rasterio as raster
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

#afflux map states
no_data = -999
same = 0            # no change in flood depth
dry_wet = 1         # was dry now is wet
wet_dry = 2         # was wet now is dry
less = 3            # flood depth is less now
more = 4            # flood depth is more now
tolerance = 0.02    # Tolerance on head water change

def main():
    dirname = os.path.dirname(__file__)
    base_path = os.path.join(dirname, "./base_scenariofia01_h_Max.asc")
    des_path = os.path.join(dirname, "./des_scenariofia01_h_Max.asc")
    base = raster.open(base_path)
    des = raster.open(des_path)

    b = base.read(1)
    d = des.read(1)
    state_field = np.zeros((len(b), len(b[0])))

    for i in range(len(b)):
        for j in range(len(b[0])):
            state_field[i][j] = flood_state(b[i][j], d[i][j])

    with raster.open(
        os.path.join(dirname, './afflux.tif'),
        'w',
        driver='GTiff',
        height=base.height,
        width=base.width,
        count=1,
        dtype=state_field.dtype,
        crs=base.crs,
        transform=base.transform,
    ) as dst:
        dst.write(state_field, 1)


def flood_state(base_value: float, des_value: float) -> int:
    if ((base_value == no_data) & (des_value == no_data)):
        return no_data
    if ((base_value + tolerance) > des_value) & ((base_value - tolerance) < des_value):
        return same
    if ((base_value == no_data) & (des_value > no_data)):
        return dry_wet
    if ((base_value > no_data) & (des_value == no_data)):
        return wet_dry
    if (base_value > des_value):
        return less
    if (base_value < des_value):
        return more
    raise FloodStateException
    

class FloodStateException(Exception):
    pass

if __name__ == "__main__":
    main()