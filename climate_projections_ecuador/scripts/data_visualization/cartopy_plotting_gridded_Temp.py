"""Plots netcdf gridded data on a basemap"""

# Import libraries
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs

# Reads netcdf data
fh = xr.open_dataset('pr_day_Ecuador_TMed_anomavg_Ensamble_mean_rcp45_2011-2040.nc')
temp = fh.variables['temp'][:]
lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]

# Squezees time dimension
temp = np.squeeze(temp)

# Sets figure size, projection and map background
fig = plt.figure(figsize=(9, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS, linestyle='-')
ax.set_title("Anomalías de Temperatura Media ($^oC$) \n período 2011-2040 (RCP4.5) ", fontsize=15)

# Formats gridlines
gl = ax.gridlines(linestyle=":", draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False

# Plots data
plt.style.use('classic')
cs = plt.contourf(lons, lats, temp,
                  transform=ccrs.PlateCarree())
# Adds scale bar
cbar = fig.colorbar(cs)

# Saves and displays figure
plt.savefig("Anom_temp_rcp4.5_2011_2040.png", dpi=300)
plt.show()
