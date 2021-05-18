#!/bin/bash

# aim to plot ATX voter precincts

# output file name
ofile=plot_shaded

# set region
reg=-R-98.19/-97.35/30.01/30.66

# set projection
proj=-JM20

# try to plot data - idea is the shapefile should be modified beforehand
# convert shp file into gmt compatible file
precincts='PropB_For'
ogr2ogr -f "GMT" $precincts.gmt $precincts.shp

# # water features
# water='misc_gis/LakesandRivers/geo_export_b18f98e7-f1fe-4607-855a-f7e510abebfd'
# ogr2ogr -f "GMT" $water.gmt $water.shp

# # streets
# streets='misc_gis/StreetCenterline/geo_export_376da4cd-f1a1-4892-bc63-3ee36ca2ffab'
# ogr2ogr -f "GMT" $streets.gmt $streets.shp

# # railroads
# railroads='misc_gis/Railroads/geo_export_5f3dc6ae-dfc3-4023-8340-3437d821e560'
# ogr2ogr -f "GMT" $railroads.gmt $railroads.shp

# identify attribute to plot
attr=For

# make colorbar
gmt makecpt -C220,150/50/50,white,50/50/150 -Z -T0,1,50,100 -Do > c.cpt

gmt psxy $precincts.gmt $reg $proj -L -Wgray -aZ=$attr -Cc.cpt -K > $ofile.ps

# # plot water features
# gmt psxy $water.gmt $reg $proj -L -Wblack -t50 -O -K >> $ofile.ps

# # plot streets
# gmt psxy $streets.gmt $reg $proj -Wblack -t75 -O -K >> $ofile.ps

# # plot railroads
# gmt psxy $railroads.gmt $reg $proj -Wthin,.- -t75 -O -K >> $ofile.ps

# add colorscale
gmt psscale -Cc.cpt -Ba25 -B+l'Prop. B "For" Vote %' -DJBC+w10c/0.5c+jTC+h+e+o0/0.75 $reg $proj -O -K >> $ofile.ps

# add text
# title
gmt pstext -R1/20/1/20 -JX17.6 \
  -F+cTC+f18+t"@_May 2021 Travis County Prop. B Election Results@_" -Qu -D0.02/0 -P -O -K >> $ofile.ps

# left area
gmt pstext -R5/10/1/5 -JX4.4 \
  -F+cTL+f12+t"@_Data Sources@_" -Qu -D0.25/0 -P -O -K >> $ofile.ps
gmt pstext -R1/20/1/20 -JX16.0 -M -F+f9 -O -K << EOF >> $ofile.ps
> 5.15 4.25 12p 2.5i l
Precinct Shapefile from the Travis County Tax Office. Election results scraped from precinct-by-precinct data provided by the Travis County Clerk. Water and railroad shapefiles from the City of Austin Open Data Portal.
EOF

# bottom right corner
echo J. Hariharan, 2021 | gmt pstext -R10/20/10/20 -JX19.75 -F+cLR -D0/0.25 \
  -P -O -K >> $ofile.ps

# try to set basemap
gmt psbasemap $reg $proj -BWSne -Tdx7.3i/6.05i+w0.8i+f2+l'','','','N' \
  -Lx0.8i/0.3i+c0+w10M -O >> $ofile.ps

# convert to eps then pdf and clean up along the way
gmt psconvert $ofile.ps -Tf -A+m0.5
rm -f $ofile.ps
rm -f $ofile.eps
