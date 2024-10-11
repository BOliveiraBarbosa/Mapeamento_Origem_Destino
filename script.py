import pandas as pd

# Dados ------------------------------------------------------------------------

radar = pd.read_csv("data/radar_areas.csv")
radar = radar[["placa_anonymized", "datahora_captura", "tipoveiculo", "nome"]]

# Tratamento dos Dados ---------------------------------------------------------

radar["tipoveiculo"] = radar["tipoveiculo"].astype("category")
radar["tipoveiculo"] = radar["tipoveiculo"].str.lower()
radar["tipoveiculo"] = radar["tipoveiculo"].str.normalize("NFKD").str.encode("ascii", errors = "ignore").str.decode("utf-8")
# TODO: Tratar mesma placa com tipos diferentes
# TODO: Tratar tipo indefinido

radar["id"] = radar["placa_anonymized"].astype('category').cat.codes

radar = radar.rename(columns = {"datahora_captura": "datetime"})

# Intersect Bairros ------------------------------------------------------------

# Função st_radar --------------------------------------------------------------

def st_radar(df, time_interval):
  """
  
  """
  
  df["datetime"] = pd.to_datetime(df["datetime"])
  
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
  
  df["caminho_st"] = df.groupby("id_st")["row"].transform(lambda x: ', '.join(x.astype(str)))
  
  df = df.drop(columns = ["id_st_local", "row"])
  
  return df

radar_st = st_radar(radar, time_interval = 3)

# Prepara Dados para Dashboard -------------------------------------------------

# Escreve Resultado ------------------------------------------------------------

radar_st.to_csv("data/origem_destino.csv")
