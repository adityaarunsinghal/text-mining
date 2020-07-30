
```{r}
install.packages('rjson')
library(httr)
library(rjson)
library(jsonlite)
library(ggplot2)
```


```{r}
json_data <- fromJSON(txt='/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/All Data/Takeout (google data +fitbit exports)/google location data for OH notebook/Location History/Location History.json')

trial_json = fromJSON("/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/All Data/Takeout (google data +fitbit exports)/google location data for OH notebook/Location History/Semantic Location History/2019/2019_JANUARY.json")
timeline = trial_json$timelineObjects
```

```{r}
# extracting the locations dataframe
loc = json_data$locations
```

```{r}
# converting time column from posix milliseconds into a readable time scale
loc$time = as.POSIXct(as.numeric(json_data$locations$timestampMs)/1000, origin = "1970-01-01")
```

```{r}
# converting longitude and latitude from E7 to GPS coordinates
loc$lat = loc$latitudeE7 / 1e7
loc$lon = loc$longitudeE7 / 1e7

tail(loc)
```

```{r}
install.packages('ggmap')
library(lubridate)
library(zoo)

loc$date <- as.Date(loc$time, '%Y/%m/%d')
loc$year <- year(loc$date)
loc$month_year <- as.yearmon(loc$date)

points_p_day <- data.frame(table(loc$date), group = "day")
points_p_month <- data.frame(table(loc$month_year), group = "month")
points_p_year <- data.frame(table(loc$year), group = "year")
```

```{r}
# set up plotting theme
library(ggplot2)
library(ggmap)

my_theme <- function(base_size = 12, base_family = "sans"){
  theme_grey(base_size = base_size, base_family = base_family) +
  theme(
    axis.text = element_text(size = 12),
    axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1),
    axis.title = element_text(size = 14),
    panel.grid.major = element_line(color = "grey"),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "aliceblue"),
    strip.background = element_rect(fill = "lightgrey", color = "grey", size = 1),
    strip.text = element_text(face = "bold", size = 12, color = "navy"),
    legend.position = "right",
    legend.background = element_blank(),
    panel.margin = unit(.5, "lines"),
    panel.border = element_rect(color = "grey", fill = NA, size = 0.5)
  )
}
```


```{r}
points <- rbind(points_p_day[, -1], points_p_month[, -1], points_p_year[, -1])
```

```{r}
ggplot(points, aes(x = group, y = Freq)) + 
  geom_point(position = position_jitter(width = 0.2), alpha = 0.3) + 
  geom_boxplot(aes(color = group), size = 0.25, outlier.colour = NA) + 
  facet_grid(group ~ ., scales = "free") + my_theme() +
  theme(
    legend.position = "none",
    strip.placement = "outside",
    strip.background = element_blank(),
    strip.text = element_blank(),
    axis.text.x = element_text(angle = 0, vjust = 0.5, hjust = 0.5)
  ) +
  labs(
    x = "",
    y = "Number of data points",
    title = "How many data points did Google collect about me?",
    subtitle = "Number of data points per day, month and year"
  )
+
  ggsave("/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/Figures saved from analyses/GoogleLocationHistory - How many points.png")

```


```{r}
accuracy <- data.frame(accuracy = loc$accuracy, group = ifelse(loc$accuracy < 500, "high", ifelse(loc$accuracy < 5000, "middle", "low")))

accuracy$group <- factor(accuracy$group, levels = c("high", "middle", "low"))

ggplot(accuracy, aes(x = accuracy, fill = group)) + 
  geom_histogram() + 
  facet_grid(group ~ ., scales="free") + 
  my_theme() +
  theme(
    legend.position = "none",
    strip.placement = "outside",
    strip.background = element_blank(),
    axis.text.x = element_text(angle = 0, vjust = 0.5, hjust = 0.5)
  ) +
  labs(
    x = "Accuracy in metres",
    y = "Count",
    title = "How accurate is the location data?",
    subtitle = "Histogram of accuracy of location points",
    caption = "\nMost data points are pretty accurate, 
but there are still many data points with a high inaccuracy.
    These were probably from areas with bad satellite reception."
  )

+
  ggsave(filename = "/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/Figures saved from analyses/GoogleLocationHistory - Accuracy.png")
```


```{r}
options(warn = -1)
world <- get_map(location=c(-179,-60,179,67), source = "stamen",maptype='toner')
ggmap(world) + 
    geom_point(data = loc, aes(x=lon, y=lat), size=0.8,alpha=0.7,color='red') + 
    #stat_density_2d(geom = "point", data = loc, aes(x=lon, y=lat, size = stat(density)), n = 20, contour = FALSE)
    #geom_density_2d(bins = 300, data = loc, aes(x = lon, y = lat), alpha = 0.5, color='red') + 
  #stat_summary_2d(geom = "tile", bins = 300, data = loc, aes(x = lon, y = lat, z = accuracy), alpha = 0.5) + 
  #scale_fill_gradient(low = "blue", high = "red", guide = guide_legend(title = "Accuracy")) +
 labs(
    x = "Longitude", 
    y = "Latitude", 
    title = "Location history data points around the world")
+
  ggsave("/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/Figures saved from analyses/GoogleLocationHistory - WorldMap.png")
```

```{r}

loc_2 <- loc[which(!is.na(loc$velocity)), ]
loc_2 <- subset(loc_2, loc_2$velocity > 0)

india = get_map("India", maptype='terrain', zoom = 10)

ggmap(india) + geom_point(data = loc_2, aes(x = lon, y = lat, color = velocity), alpha = 0.1,size=0.5) +
  theme(legend.position = "right") +
  labs(x = "Longitude", y = "Latitude",
       title = "Location history data points in India",
       subtitle = "Color scale shows velocity measured for location") +
  scale_colour_gradient(low = "blue", high = "red", guide = guide_legend(title = "Velocity")) +
  ggsave("/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/Figures saved from analyses/GoogleLocationHistory - IndiaMap.png")

# frankfurt_boundary_west=8.6
# frankfurt_boundary_east=8.8
# frankfurt_boundary_south=50.075
# frankfurt_boundary_north=50.20
# 
# loc_2 <- loc[which(!is.na(loc$velocity)), ]
# loc_2 <- subset(loc_2, loc_2$velocity > 0)
# frankfurt <- get_map(location=c(
#     frankfurt_boundary_west,
#     frankfurt_boundary_south,
#     frankfurt_boundary_east,
#     frankfurt_boundary_north), source = "stamen",maptype='toner')
# ggmap(frankfurt) + geom_point(data = loc_2, aes(x = lon, y = lat, color = velocity), alpha = 0.3,size=0.7) + 
#   theme(legend.position = "right") + 
#   labs(x = "Longitude", y = "Latitude", 
#        title = "Location history data points in Frankfurt",
#        subtitle = "Color scale shows velocity measured for location") +
#   scale_colour_gradient(low = "blue", high = "red", guide = guide_legend(title = "Velocity"))
# 
# berkeley_boundary_west=-122.325
# berkeley_boundary_east=-122.23
# berkeley_boundary_south=37.84
# berkeley_boundary_north=37.89
```
```{r}
install.packages("writexl")
library(writexl)

write_xlsx(loc,"/Users/aditya/Google Drive (as11919@nyu.edu)/Syncing with Mac/My Data Analysis/All Data/Takeout (google data +fitbit exports)/GoogleLocationHistory(Aug2013-July2020).xlsx")

class(loc)
```


```{r}
# loc_2 <- loc[which(!is.na(loc$velocity)), ]
# loc_2 <- subset(loc_2, loc_2$velocity > 0)
# berkeley <- get_map(location=c(berkeley_boundary_west,
#                                berkeley_boundary_south,
#                                berkeley_boundary_east,
#                                berkeley_boundary_north), source = "stamen",maptype='toner')
# ggmap(berkeley) + geom_point(data = loc_2, aes(x = lon, y = lat, color = velocity), alpha = 0.3,size=0.7) + 
#   theme(legend.position = "right") + 
#   labs(x = "Longitude", y = "Latitude", 
#        title = "Location history data points in Berkeley",
#        subtitle = "Color scale shows velocity measured for location") +
#   scale_colour_gradient(low = "blue", high = "red", guide = guide_legend(title = "Velocity"))
```