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

# produce water accumulation rasters and store them in a tuple
accum_d8 = rd.FlowAccumulation(dem_rdarray, method='D8')
accum_rho8 = rd.FlowAccumulation(dem_rdarray, method='Rho8')
accum_d_inf = rd.FlowAccumulation(dem_rdarray, method='Dinf')

accum_tuple = (('D8', accum_d8),
               ('Rho8', accum_rho8),
               ('D_inf', accum_d_inf))

# save each map as a png
for plot_id, accum_map in enumerate(accum_tuple):
    fig, ax = plt.subplots()
    vmin, vmax = np.nanpercentile(accum_map[1], [2, 98])
    plot = ax.imshow(accum_map[1], vmin=vmin, vmax=vmax, cmap='jet')
    ax.set_title(accum_map[0])
    cax = fig.add_axes([ax.get_position().x1 + 0.01,
                        ax.get_position().y0, 0.02,
                        ax.get_position().height])
    fig.colorbar(plot, cax=cax)
    plt.savefig(f'{pth_topography}/water_accumulation_map_{accum_map[0]}.png', dpi=200)

# save all maps on single png for comparison
fig, axes = plt.subplots(ncols=1, nrows=len(accum_tuple))
for plot_id, accum_map in enumerate(accum_tuple):
    vmin, vmax = np.nanpercentile(accum_map[1], [2, 98])
    plot = axes[plot_id].imshow(accum_map[1], vmin=vmin, vmax=vmax, cmap='jet')
    cax = fig.add_axes([axes[plot_id].get_position().x1 + 0.01,
                        axes[plot_id].get_position().y0, 0.02,
                        axes[plot_id].get_position().height])
    fig.colorbar(plot, cax=cax)
    axes[plot_id].set_title(accum_map[0])
plt.savefig(f'{pth_topography}/water_accumulation_map_comparison.png', dpi=200)
plt.show()
