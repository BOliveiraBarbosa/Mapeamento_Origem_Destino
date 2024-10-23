import contextily
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Dados ------------------------------------------------------------------------

areas = gpd.read_file("data/limite_de_bairros.geojson")
areas = areas[["nome", "geometry"]]

radar = pd.read_csv("data/ocr_radar.csv")

# Tratamento dos Dados ---------------------------------------------------------

radar["tipoveiculo"] = radar["tipoveiculo"].astype("category")
radar["tipoveiculo"] = radar["tipoveiculo"].str.lower()
radar["tipoveiculo"] = radar["tipoveiculo"].str.normalize("NFKD").str.encode("ascii", errors = "ignore").str.decode("utf-8")

radar["id"] = radar["placa_anonymized"].astype('category').cat.codes

radar_classe = radar[radar["tipoveiculo"] != "indefinido"].groupby(["id", "tipoveiculo"]).size().reset_index(name = "counts")
radar_classe = radar_classe.loc[radar_classe.groupby("id")["counts"].idxmax()]
radar_classe = radar_classe[["id", "tipoveiculo"]]
radar = pd.merge(radar, radar_classe, how = "left", on = "id", suffixes = ("", "_final"))

radar = radar.rename(columns = {"datahora_captura": "datetime"})
radar["datetime"] = pd.to_datetime(radar["datetime"])

# Intersect Bairros ------------------------------------------------------------

radar = gpd.GeoDataFrame(
  radar, 
  geometry = gpd.points_from_xy(radar.camera_longitude, radar.camera_latitude),
  crs = 4674
)

radar_areas = gpd.overlay(radar, areas, how = "intersection")

radar_areas["x"] = radar_areas.geometry.x
radar_areas["y"] = radar_areas.geometry.y

radar_areas = radar_areas.drop(columns = "geometry")

# Função st_radar --------------------------------------------------------------

def st_radar(df, time_interval):
  """
  
  """
  
  df = df.sort_values(by = ["id", "datetime"])
  
  def add_id_st(group):
    """
    """
    
    group = group.sort_values(by = "datetime")
    group["id_st_local"] = (group["datetime"].diff() > pd.Timedelta(hours = time_interval)).cumsum() + 1
    group["id_st"] = group["id"].astype(str) + '_' + group["id_st_local"].astype(str)
    return group

  df = df.groupby("id").apply(add_id_st).reset_index(drop = True)
  
  df.reset_index(inplace = True)
  df.rename(columns = {"index": "row"}, inplace = True)
  
  df["caminho_st"] = df.groupby("id_st")["row"].transform(lambda x: ", ".join(x.astype(str)))
  
  df = df.drop(columns = ["id_st_local", "row"])
  
  return df

radar_st = st_radar(radar_areas, time_interval = 3)

# Plot Mapa --------------------------------------------------------------------

fig, ax = plt.subplots()
ax.plot(radar_st.x, radar_st.y, "o", markersize = 1)
contextily.add_basemap(ax, crs = 4674)
plt.show()

# Conatagem Origem-Destino -----------------------------------------------------



# Escreve Resultado ------------------------------------------------------------

radar_st.to_csv("data/origem_destino.csv")
