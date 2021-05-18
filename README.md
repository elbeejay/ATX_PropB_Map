# ATX_PropB_Map
Semi-automated workflow to create a map of precinct-by-precinct election results for Austin, TX

![Final Map](plot_shaded.png)

This repository provides the source code necessary to reproduce the map shown above. Technical step-by-step instructions required to reproduce this map are provided below, for a more qualitative explanation of the map and project see [this page](https://jayaramhariharan.com/).

## Data Sources
Data for this project comes from a variety of Travis County and City of Austin resources.

- The original Travis County precinct shapefile was obtained from the [Travis County Tax Office](https://tax-office.traviscountytx.gov/about-us/reports-data/voters), the provided [TECP_reprojected_mod.shp](TECP_reprojected_mod.shp) shapefile has been re-projected to a more common projection so that it works better with GMT
- Unofficial local election results were obtained from the [Travis County Clerk](https://countyclerk.traviscountytx.gov/elections/election-results-1/results-for-may-01-2021-local-elections.html)
- Miscellaneous GIS data from the [City of Austin Open Data Portal](https://data.austintexas.gov/), more information on this GIS data as it can be used in this project is available [here](misc_gis/README.md)

## Software and Packages Required
The Python processing requires the following libraries (also in [requirements.txt](requirements.txt)):

- `numpy`
- `pandas`
- `matplotlib`
- `tabula`
- `geopandas`

Generating the map itself requires [GMT](https://www.generic-mapping-tools.org/) (I used GMT 6.0.0).
Within the GMT script, [GDAL](https://gdal.org/) and [ghostscript](https://ghostscript.com/) are used. 
Post-processing to go from an output PDF to a `.png` image was done with [ImageMagick](https://imagemagick.org/index.php).

## Workflow
- [Scrape the Election Results PDF](Scrape-the-Election-Results-PDF)
- [Associate Scraped Data to Geographical Data](Associate-Scraped-Data-to-Geographical-Data)
- [Create the Map with GMT](Create-the-Map-with-GMT)
- [Post-Process to an image](Post-Process-to-an-image)

### Scrape the Election Results PDF 

### Associate Scraped Data to Geographical Data

### Create the Map with GMT

Within the GMT script, [GDAL](https://gdal.org/) is required to convert shapefiles to GMT-compatible files, and [ghostscript](https://ghostscript.com/) is necessary to convert the PostScript output file into a PDF. 

### Post-Process to an image

To post-process the output PDF into a `.png` image file, I used the following [ImageMagick](https://imagemagick.org/index.php) CLI command:
```
convert -density 300 plot_shaded.pdf -flatten plot_shaded.png
```
