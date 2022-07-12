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
scenarios = ['1p', '2p', '5p']

def main():
    dirname = os.path.dirname(__file__)
    land_path = os.path.join(dirname, "surface.asc")
    land = raster.open(land_path)
    l = land.read(1)

    for s in scenarios:
        base_name, des_name = concate_scenario(s)
        base_path = os.path.join(dirname, base_name)
        des_path = os.path.join(dirname, des_name)
        base = raster.open(base_path)
        des = raster.open(des_path)

        b = base.read(1)
        d = des.read(1)
        state_field = np.zeros((len(b), len(b[0])))
        scalar_field = state_field.copy()

        for i, (bp, dp, lp) in enumerate(zip(b, d, l)):
            for j, (bpp, dpp, lpp) in enumerate(zip(bp, dp, lp)):
                state_field[i][j], scalar_field[i][j] = flood_state(bpp, dpp, lpp)

        with raster.open(
            os.path.join(dirname, f"afflux_bands{s}.tif"),
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
    return (f"base_scenario{s}01_h_Max.asc", f"des_scenario{s}01_h_Max_3culvert_drop.asc")

class FloodStateException(Exception):
    pass

if __name__ == "__main__":
    main()
