import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from unidecode import unidecode

radar = pd.read_csv("data/ocr_radar.csv", date_format = ["datahora_captura", "datahora"])

# Plot Frequência Veículos -----------------------------------------------------

fig, ax = plt.subplots(figsize = (8, 4))
sns.countplot(data = radar, x = "tipoveiculo", ax = ax)
plt.show()

# Limpeza da Categoria "tipoveiculo"" ------------------------------------------

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

df = df[df["count"] >= 2]

radar_filter = pd.merge(df, radar, on = "placa_anonymized", how = "left")

# TODO: pegar todos os 5M de linhas

# Contagem placa Véiculo--------------------------------------------------------

contagem_placa_veiculo = radar.groupby(["placa_anonymized", "tipoveiculo"], as_index = False).agg(
  count = pd.NamedAgg(column = "placa_anonymized", aggfunc = "count")
)

# ------------------------------------------------------------------------------

# TODO: Fazer st, tentar separar com varios valores 1h, 2h, 3h

# TODO: plot radar shape
