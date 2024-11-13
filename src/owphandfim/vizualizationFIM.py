import os
import geemap
import numpy as np
import rasterio
import geopandas as gpd
from ipyleaflet import WidgetControl
from ipywidgets import HTML

from .datadownload import setup_directories


def FIMVizualizer(raster_path, catchment_gpkg, zoom_level):
    with rasterio.open(raster_path) as src:
        data = src.read(1)
        binary_data = np.where(data > 0, 1, 0)

        # Creating a new raster with binary data
        new_raster_path = raster_path.replace(".tif", "_binary.tif")
        with rasterio.open(
            new_raster_path,
            "w",
            driver="GTiff",
            height=src.height,
            width=src.width,
            count=1,
            dtype=np.uint8,
            crs=src.crs,
            transform=src.transform,
        ) as dst:
            dst.write(binary_data.astype(np.uint8), 1)

    # Dissolve catchments into one boundary extent from the GeoPackage
    catchment_gdf = gpd.read_file(catchment_gpkg)
    dissolved_catchment = catchment_gdf.dissolve()

    # Initialize the map
    Map = geemap.Map()
    Map.add_basemap("SATELLITE", layer_name="Google Satellite")

    # HUC Boundary
    Map.add_gdf(
        dissolved_catchment,
        layer_name="HUC Boundary",
        style={"fillColor": "none", "color": "Red", "weight": 2.5, "dashArray": "5, 5"},
    )

    # Binary Raster
    Map.add_raster(
        new_raster_path,
        colormap="Blues",
        layer_name="Flood Inundation Extent",
        nodata=0,
    )

    # Set the zoom level
    center = dissolved_catchment.geometry.centroid.iloc[0]
    Map.set_center(center.x, center.y, zoom=zoom_level)

    legend_html = """
    <div style="font-size: 16px; line-height: 1.5;">
        <strong>Legend</strong><br>
        <div><span style="display:inline-block; width: 25px; height: 15px; background-color: #1c83eb; border: 1px solid #000;"></span>FIM Extent</div>
        <div><span style="display:inline-block; width: 25px; height: 15px; border: 2px dashed red; margin-right: 5px;"></span>HUC8  Boundary</div>
    </div>
    """

    # Add the HTML legend to the map
    legend_widget = HTML(value=legend_html)
    legend_control = WidgetControl(widget=legend_widget, position="bottomright")
    Map.add_control(legend_control)

    return Map


def vizualizeFIM(inundation_raster, huc, zoom_level):
    code_dir, data_dir, output_dir = setup_directories()
    HUCBoundary = os.path.join(
        output_dir,
        f"flood_{huc}",
        f"{huc}",
        "branches",
        "0",
        "gw_catchments_reaches_filtered_addedAttributes_0.gpkg",
    )
    return FIMVizualizer(inundation_raster, HUCBoundary, zoom_level)
