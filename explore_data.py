from pathlib import Path
from osgeo import gdal
import matplotlib.pyplot as plt
import geopandas as gpd
from info import pth_topography, pth_vegetation

pth_ndvi = Path(pth_vegetation, 'Points_vigueur_Greenseeker_NDVI_2011_2019')
pth_zoning = Path(pth_vegetation, 'Zonage_NDVI_2011_2019_EVI_2020')
year = 2019

# Load shapefiles
ndvi_shp = gpd.read_file(f'{pth_ndvi}/RS-NDVI-{year}-sup02-l93.shp')
zoning_shp = gpd.read_file(f'{pth_zoning}/Zonage_Rieussec_{year}_VF.shp')

# summarize data
nb_plots = ndvi_shp['code_pg'].unique().__len__()
for key, group in ndvi_shp.groupby(by=['code_pg', 'nom_var']):
    print(f"{key}: {group['Date'].unique()} ({group['Date'].unique().size} mesure(s))")

# display .tiff
file_name = 'Altitude_TIN_autocad_Rieussec_low_res'
data_altitude = gdal.Open(f'{pth_topography}/{file_name}.tif')
data_test = data_altitude.GetRasterBand(1).ReadRaster()
f = plt.figure()
plt.imshow(data_altitude.GetRasterBand(1).ReadAsArray())
plt.savefig(f'{pth_topography}/{file_name}.png')
plt.show()
