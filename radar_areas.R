library(tidyverse)
library(sf)

areas <- read_sf("data/limite_de_bairros.geojson", crs = 4674) %>% 
  select(nome)

radar <- read_csv("data/ocr_radar.csv") %>% 
  st_as_sf(
    coords = c("camera_longitude", "camera_latitude"), 
    crs = 4674
  )

radar_areas <- st_intersection(radar, areas) %>% 
  mutate(
    lon = sf::st_coordinates(.)[,1],
    lat = sf::st_coordinates(.)[,2]
  ) %>% 
  st_drop_geometry()

write_csv(radar_areas, "data/radar_areas.csv")
