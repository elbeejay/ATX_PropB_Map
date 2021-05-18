"""Python script to add vote information to the precinct shapefile."""
import geopandas as gpd
import pandas as pd
import numpy as np

# load the shapefile that has been nicely reprojected
shp = gpd.read_file('TECP_reprojected_mod.shp')

# load the dataframe with scraped vote data
df = pd.read_csv('ScrapedResults_PropB_perPrecinct.csv')

# add column for "for" votes
shp['For'] = np.nan

# set values where we have them
for i in shp['PCT']:
    # see where we have data
    if int(i) in list(df['Precinct']):
        # get index in shp
        shp_ind = np.where(shp['PCT']==i)[0][0]
        # get index in df
        df_ind = np.where(df['Precinct']==int(i))[0][0]
        # get value from df using index
        df_val = df['For'][df_ind]
        # place value into correct location using shp index
        shp['For'][shp_ind] = df_val

# write out the new shapefile with propB "for" vote info
shp.to_file('PropB_For.shp')
