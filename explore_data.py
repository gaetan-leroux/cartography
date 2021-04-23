from pathlib import Path

import geopandas as gpd

pth_vegetation = Path('data/Vegetation')
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

print('')
