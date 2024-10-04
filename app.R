library(shiny)
library(tidyverse)
library(sf)
library(leaflet)
library(leafpop)
library(shinydashboard)

icon_radar <- makeIcon(
  iconUrl = "https://cdn.icon-icons.com/icons2/390/PNG/512/cctv-camera_39530.png",
  iconWidth = 15, iconHeight = 30,
)

radar_areas <- read_csv("data/radar_areas.csv") %>% 
  group_by(nome, lon, lat) %>% 
  summarise(registros = n()) %>% 
  st_as_sf(coords = c("lon", "lat"), crs = 4674)

areas <- st_read("data/limite_de_bairros.geojson", crs = 4674)
 
ui <- fluidPage(
  inputPanel(
    selectInput(
      inputId = "bairro",
      label = "Bairro",
      choices = c("Todos", areas %>% st_drop_geometry() %>% select(nome) %>% arrange(nome)),
      selected = "Todos"
    )
  ),
  mainPanel(width = 12,
    tags$head(tags$style("#map{height:85vh !important;}")),
    leafletOutput("map")
  )
)

server <- function(input, output) {
  
  output$map <- renderLeaflet({
    leaflet() %>% 
      addTiles() %>% 
      leaflet::addPolygons(
        data = areas,
        color = "#740024",
        fillColor = "#d5d4b6",
        fillOpacity = 0,
        opacity = 1,
        stroke = TRUE,
        smoothFactor = 1,
        weight = 1.8,
        popup = popupTable(areas, row.numbers = FALSE, feature.id = FALSE)
      )
  })
  
  observe({
    data <- radar_areas %>% 
      filter(nome == input$bairro | input$bairro == "Todos")
    
    if(nrow(data) == 0) {
      leaflet::leafletProxy("map") %>% 
        leaflet::clearGroup("radar_areas")
    } else {
      leaflet::leafletProxy("map") %>% 
        leaflet::clearGroup("radar_areas") %>% 
        addMarkers(
          data = data,
          icon = icon_radar,
          group = "radar_areas",
          popup = popupTable(data, row.numbers = FALSE, feature.id = FALSE),
        )
    }
  })
}

shinyApp(ui = ui, server = server)
