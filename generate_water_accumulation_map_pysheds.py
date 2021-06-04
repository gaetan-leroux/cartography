from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pysheds.grid import Grid

from info import pth_topography

# Load DEM (Digital Elevation Map = altitude map) raster
dem_file = 'Altitude_TIN_autocad_Rieussec_low_res.tif'
grid = Grid.from_raster(f'{pth_topography}/{dem_file}', data_name='dem')

# Resolve flats in DEM: associate flow direction to a zone that locally doesn't have any elevation gradient (flat)
grid.resolve_flats('dem', out_name='inflated_dem')

# Define directional mapping for d8 flow direction function
dirmap_d8 = (64, 128, 1, 2, 4, 8, 16, 32)

# Compute flow directions
grid.flowdir(data='dem', out_name='dir_d8', dirmap=dirmap_d8)
grid.flowdir(data='dem', out_name='dir_dinf', routing='dinf')
grid.flowdir(data='inflated_dem', out_name='dir_d8_inflated', dirmap=dirmap_d8)
grid.flowdir(data='inflated_dem', out_name='dir_dinf_inflated', routing='dinf')

# Compute water accumulation rasters and store them in a dictionary
grid.accumulation(data='dir_d8', dirmap=dirmap_d8, out_name='accum_d8')
grid.accumulation(data='dir_dinf', out_name='accum_dinf', routing='dinf')
grid.accumulation(data='dir_d8_inflated', dirmap=dirmap_d8, out_name='accum_d8_inflated')
grid.accumulation(data='dir_dinf_inflated', out_name='accum_dinf_inflated', routing='dinf')

accum_dict = {'accum_d8': {'accum': grid.accum_d8, 'x': 0, 'y': 0},
              'accum_dinf': {'accum': grid.accum_dinf, 'x': 0, 'y': 1},
              'accum_d8_inflated': {'accum': grid.accum_d8_inflated, 'x': 1, 'y': 0},
              'accum_dinf_inflated': {'accum': grid.accum_dinf_inflated, 'x': 1, 'y': 1}}

# Display accumulation rasters in a single plot for comparison
fig, axes = plt.subplots(ncols=2, nrows=2)
for _, accum_method in enumerate(accum_dict):
    acc_dict = accum_dict[accum_method]
    vmin, vmax = np.nanpercentile(acc_dict['accum'], [2, 98])
    plot = axes[acc_dict['x']][acc_dict['y']].imshow(acc_dict['accum'], vmin=vmin, vmax=vmax, cmap='jet')
    cax = fig.add_axes([axes[acc_dict['x']][acc_dict['y']].get_position().x1 + 0.01,
                        axes[acc_dict['x']][acc_dict['y']].get_position().y0, 0.02,
                        axes[acc_dict['x']][acc_dict['y']].get_position().height])
    fig.colorbar(plot, cax=cax)
    axes[acc_dict['x']][acc_dict['y']].set_title(accum_method)

if not Path.exists(Path(f'{pth_topography}/pysheds')):
    Path(f'{pth_topography}/pysheds').mkdir(exist_ok=True)
plt.suptitle('Flow accumulation map with Pysheds package')
plt.savefig(f'{pth_topography}/pysheds/water_accumulation_map_comparison.png', dpi=200)
plt.show()
