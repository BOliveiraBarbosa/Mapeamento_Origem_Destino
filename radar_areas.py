import geopandas as gpd
import matplotlib.pyplot as plt

areas = gpd.read_file("data/limite_de_bairros.geojson")

areas.head()

areas.plot()
plt.show()


areas = areas[["nome", "geometry"]]

radar = pd.read_csv("data/ocr_radar.csv")

radar = gpd.GeoDataFrame(
  radar, 
  geometry = gpd.points_from_xy(radar.camera_longitude, radar.camera_latitude),
  crs = 4674
)

radar_areas = gpd.overlay(radar, areas, how = 'intersection')

radar_areas['lon'] = radar_areas.geometry.x
radar_areas['lat'] = radar_areas.geometry.y

radar_areas = radar_areas.drop(columns = 'geometry')
radar_areas.to_csv("data/radar_areas.csv", index = False)
