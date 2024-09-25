import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium

radar = pd.read_csv("data/ocr_radar.csv", date_format = ["datahora_captura", "datahora"])

# Plot Frequência Veículos -----------------------------------------------------

fig, ax = plt.subplots(figsize = (8, 4))
sns.countplot(data = radar, x = "tipoveiculo", ax = ax)
plt.show()

# Limpeza da Categoria "tipoveiculo" -------------------------------------------

radar["tipoveiculo"] = radar["tipoveiculo"].astype("category")
radar["tipoveiculo"] = radar["tipoveiculo"].str.lower()
radar["tipoveiculo"] = radar["tipoveiculo"].str.normalize("NFKD").str.encode("ascii", errors = "ignore").str.decode("utf-8")

radar["tipoveiculo"].value_counts(dropna = False)

# Plot Frequência Veículos -----------------------------------------------------

fig, ax = plt.subplots(figsize = (8, 4))
sns.countplot(data = radar, x = "tipoveiculo", ax = ax)
plt.show()

# Veículos Com Mais de um registro ---------------------------------------------

df = radar.groupby("placa_anonymized", as_index = False).agg(
  count = pd.NamedAgg(column = "placa_anonymized", aggfunc = "count")
)

df = df[df["count"] > 1]

radar_filter = pd.merge(df, radar, on = "placa_anonymized", how = "left")

# Contagem placa Véiculo -------------------------------------------------------

contagem_placa_veiculo = radar.groupby(["placa_anonymized", "tipoveiculo"], as_index = False).agg(
  count = pd.NamedAgg(column = "placa_anonymized", aggfunc = "count")
)

# Plot radar shape -------------------------------------------------------------

radar_unico = radar.drop_duplicates(subset = ["camera_latitude", "camera_longitude"])
radar_unico = radar_unico[["camera_latitude", "camera_longitude"]]

radar_unico_list = radar_unico.values.tolist()

map = folium.Map(location = [38.9, -77.05], zoom_start=12)

for point in range(0, len(radar_unico_list)):
    folium.Marker(radar_unico_list[point]).add_to(map)

map.save("img/index.html")
