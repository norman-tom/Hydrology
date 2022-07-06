"""
Author: Tom Norman 
Licence GPL3
Description:
script to produce flood afflux maps from existing scenario (base) and design scenario.
Base a design rasters must have the same crs and extent.
scenario array specifies which maps the afflux maps are to be produced for. Assuming the standard Tuflow output format. 
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
scenarios = ['100y', '020y', '010y']

def main():
    dirname = os.path.dirname(__file__)
    land_path = os.path.join(dirname, "ACT_CRK_002_100y+120m+TP1_DEM_Z.asc")
    land = raster.open(land_path)
    l = land.read(1)

    for s in scenarios:
        base_path = os.path.join(dirname, concate_scenario(s)[0])
        des_path = os.path.join(dirname, concate_scenario(s)[1])
        base = raster.open(base_path)
        des = raster.open(des_path)

        b = base.read(1)
        d = des.read(1)
        state_field = np.zeros((len(b), len(b[0])))
        scalar_field = state_field.copy()

        for i in range(len(b)):
            for j in range(len(b[0])):
                ret = flood_state(b[i][j], d[i][j], l[i][j])
                state_field[i][j] = ret[0]
                scalar_field[i][j] = ret[1]

        with raster.open(
            os.path.join(dirname, "afflux_bands{}.tif".format(s)),
            'w',
            driver='GTiff',
            height=base.height,
            width=base.width,
            count=2,
            dtype=state_field.dtype,
            crs=base.crs,
            transform=base.transform,
        ) as dst:
            dst.write(state_field, 1)
            dst.write(scalar_field, 2)

def flood_state(base_value: float, des_value: float, land_value: float) -> int:
    if ((base_value == no_data) & (des_value == no_data)):
        return (no_data, no_data)
    if ((base_value + tolerance) > des_value) & ((base_value - tolerance) < des_value):
        return (same, 0)
    if ((base_value == no_data) & (des_value > no_data)):
        return (dry_wet, (des_value - land_value))
    if ((base_value > no_data) & (des_value == no_data)):
        return (wet_dry, land_value - base_value)
    if (base_value > des_value):
        return (less, (des_value - base_value))
    if (base_value < des_value):
        return (more, (des_value - base_value))
    raise FloodStateException
    
def concate_scenario(s):
    x = "360m"
    if s == "100y":
        x = "120m"

    return ("ACT_CRK_002_{}+{}+TP1_h_Max_base.asc".format(s, x), "ACT_CRK_002_{}+{}+TP1_h_Max_fill.asc".format(s, x))

class FloodStateException(Exception):
    pass

if __name__ == "__main__":
    main()
