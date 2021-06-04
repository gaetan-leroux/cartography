from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import richdem as rd
from osgeo import gdal

from info import pth_topography

# Load DEM (Digital Elevation Map = altitude map) into a numpy.ndarray
dem_file = 'Altitude_TIN_autocad_Rieussec_low_res.tif'
dem = gdal.Open(f'{pth_topography}/{dem_file}')
dem_array = dem.GetRasterBand(1).ReadAsArray()

# richdem package requires specific array format (even though numpy.ndarray was supposed to be allowed in doc...)
dem_rdarray = rd.rdarray(dem_array, no_data=-9999)

# produce water accumulation rasters and store them in a dictionary
accum_d8 = rd.FlowAccumulation(dem_rdarray, method='D8')
accum_rho8 = rd.FlowAccumulation(dem_rdarray, method='Rho8')
accum_d_inf = rd.FlowAccumulation(dem_rdarray, method='Dinf')

accum_dict = {'accum_d8': {'acc': accum_d8, 'x': 0, 'y': 0},
              'accum_rho8': {'acc': accum_rho8, 'x': 0, 'y': 1},
              'accum_d_inf': {'acc': accum_d_inf, 'x': 1, 'y': 0}}

# save each map as a png
for _, acc_method in enumerate(accum_dict):
    fig, ax = plt.subplots()
    acc_dict = accum_dict[acc_method]
    vmin, vmax = np.nanpercentile(acc_dict['acc'], [2, 98])
    plot = ax.imshow(acc_dict['acc'], vmin=vmin, vmax=vmax, cmap='jet')
    ax.set_title(acc_method)
    cax = fig.add_axes([ax.get_position().x1 + 0.01,
                        ax.get_position().y0, 0.02,
                        ax.get_position().height])
    fig.colorbar(plot, cax=cax)
    if not Path.exists(Path(f'{pth_topography}/richdem')):
        Path(f'{pth_topography}/richdem').mkdir(exist_ok=True)
    plt.savefig(f'{pth_topography}/richdem/water_accumulation_map_{acc_method}.png', dpi=200)

# save all maps on single png for comparison
fig, axes = plt.subplots(ncols=2, nrows=2)
for _, acc_method in enumerate(accum_dict):
    acc_dict = accum_dict[acc_method]
    vmin, vmax = np.nanpercentile(acc_dict['acc'], [2, 98])
    plot = axes[acc_dict['x']][acc_dict['y']].imshow(acc_dict['acc'], vmin=vmin, vmax=vmax, cmap='jet')
    cax = fig.add_axes([axes[acc_dict['x']][acc_dict['y']].get_position().x1 + 0.01,
                        axes[acc_dict['x']][acc_dict['y']].get_position().y0, 0.02,
                        axes[acc_dict['x']][acc_dict['y']].get_position().height])
    fig.colorbar(plot, cax=cax)
    axes[acc_dict['x']][acc_dict['y']].set_title(acc_method)
if not Path.exists(Path(f'{pth_topography}/richdem')):
    Path(f'{pth_topography}/richdem').mkdir(exist_ok=True)
plt.suptitle('Flow accumulation map with Richdem package')
plt.savefig(f'{pth_topography}/richdem/water_accumulation_map_comparison.png', dpi=200)
plt.show()
