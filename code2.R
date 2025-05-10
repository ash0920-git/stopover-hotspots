#Landcover
library(sf)
library(dplyr)
library(ggplot2)
sites <- st_read("D:/R/bu_glance_training_dataV1.geojson")
data <- data.frame(
  lon = sites$Lon,
  lat = sites$Lat,
  Glance_Class_ID_level1 = sites$Glance_Class_ID_level1,
  Glance_Class_ID_level2 = sites$Glance_Class_ID_level2
)
library(terra)
points <- vect(data, geom = c("lon", "lat"), crs = "EPSG:4326") 
raster_template <- rast(ext(points), resolution = 0.5, crs = crs(points))
r <- rasterize(points, raster_template, field = "Glance_Class_ID_level1")
writeRaster(r, "D:/R/GLanCE_1.tif", overwrite = TRUE)
r <- rasterize(points, raster_template, field = "Glance_Class_ID_level2")
writeRaster(r, "D:/R/GLanCE_2.tif", overwrite = TRUE)

#####################
# 查看基本信息
library(terra)
library(sf)
library(readxl)
library(stringr)
Notes <- read_excel("D:/R/坐标点.xlsx")
colnames(Notes) <- c("note","XY")
Notes$XY_clean <- gsub("（|）", "", Notes$XY)
Notes$XY_clean <- gsub("，", ",", Notes$XY_clean)
coords <- str_match(Notes$XY_clean, "([0-9.\\-]+),([0-9.\\-]+)")
Notes$y <- as.numeric(coords[, 2])
Notes$x <- as.numeric(coords[, 3])
Notes$x <- Notes$x - 100000
Notes$y <- Notes$y - 100000
Notes$layer <- ifelse(Notes$note == "I", 1, 2)
Notes <- Notes[,c("x","y","layer")]
r <- rast(Notes, type = "xyz")
crs(r) <- "EPSG:3857"
p <- as.polygons(r, dissolve = FALSE)
sf_obj <- st_as_sf(p)
st_write(sf_obj, "D:/R/sf_points.shp", append = FALSE)


#read data----
#landcover
Landcover <- rast("D:/R/GLanCE_1.tif")
Landcover <- as.factor(Landcover)
Landcover_merc <- project(Landcover, "EPSG:3857")
target_res <- 50000
new_r <- rast(ext(Landcover_merc), res = target_res, crs = crs(Landcover_merc))
Landcover_m <- resample(Landcover_merc, new_r, method="near")

#hfp
hfp <- rast("D:/R/hfp2019.tif")
target_res <- 10000
new_r <- rast(ext(hfp), res = target_res, crs = crs(hfp))
hfp_m <- resample(hfp, new_r, method="bilinear")
hfp_m <- project(hfp_m, "EPSG:3857")
target_res <- 50000
new_r <- rast(ext(hfp_m), res = target_res, crs = crs(hfp_m))
hfp_m <- resample(hfp_m, new_r, method="bilinear")

#
library(data.table)
Ext <- c(-14796209.33, -7796209.33, 10799.54, 7210799.54)
landcover0 <- crop(Landcover_m, Ext)
sf_obj <- st_read("D:/R/sf_points.shp")
landcover1 <- crop(Landcover_m, sf_obj[sf_obj$layer==1,], mask=T)
landcover2 <- crop(Landcover_m, sf_obj[sf_obj$layer==2,], mask=T)
landcover_ALL <- crop(Landcover_m, sf_obj, mask=T)


points <- data.table(as.data.frame(landcover_ALL, xy=T))
colnames(points) <- c("x", "y", "group")
points$area  <- "SW"
points[which(points$y>21e5),"area"]="SE"
points[which(points$y>41e5),"area"]="NW"
DATA <- points %>%
  group_by(group, area) %>%
  summarise(
    count = n(),                      # 计数
    proportion = n() / nrow(points)        # 占总体比例
  )

write.csv(DATA, "D:/R/landcover.csv")
DATA <- read.csv("D:/R/landcover.csv")
p1 <- ggplot(DATA)+
  geom_point(aes(x=area, y=proportion, color=factor(group)))+
  theme_bw()
ggsave(p1, filename = "D:/R/landcover.pdf", width=6, height = 4)
if(F){
  i=1
  library(dplyr)
  #group = "",area = ""
  DATA <- data.frame()
  i = 2
  for(i in c(2:3)){
    r <- get(sprintf("landcover%d", i - 1))
    points <- data.table(as.data.frame(r, xy=T))
    colnames(points) <- c("x", "y", "group")
    points$area  <- "CA"
    points[which(points$y>21e5),"area"]="FL"
    points[which(points$y>41e5),"area"]="PS"
    points$var <- sprintf("landcover%d", i - 1)
    data <- points %>%
      group_by(group, area, var) %>%
      summarise(
        count = n(),                      # 计数
        proportion = n() / nrow(points)        # 占总体比例
      )
    DATA <- rbind(DATA, data)
  }
  DATA <- DATA[order(DATA$area,DATA$group), ]
}



#########################
Ext <- c(-14796209.33, -7796209.33, 10799.54, 7210799.54)
hfp0 <- crop(hfp_m, Ext)
a1 <- c(0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)
data <- data.frame(quantile = a1,
           value = quantile(values(hfp0), a1, na.rm=T))
write.csv(data, "D:/R/HFPall_quantile.csv")

hfp1 <- crop(hfp_m, sf_obj[sf_obj$layer==1,], mask=T)
hfp2 <- crop(hfp_m, sf_obj[sf_obj$layer==2,], mask=T)
DATA <- data.frame()
for(i in c(2:3)){
  r <- get(sprintf("hfp%d", i - 1))
  data <- as.data.frame(r, xy=T)
  DATA <- rbind(DATA, data)
}
hist(DATA$y)
DATA$area  <- "CA"
DATA[which(DATA$y>21e5),"area"]="FL"
DATA[which(DATA$y>41e5),"area"]="PS"
write.csv(DATA, "D:/R/hfp.csv")

DATA <- read.csv("D:/R/hfp.csv")
library(ggpubr)
data <- data.frame(quantile = a1,
                   value = quantile(values(hfp0), a1, na.rm=T))
p1 <- ggboxplot(DATA, x = "area", y = "hfp2019", add = "jitter") +
  geom_hline(data = data, aes(yintercept = value), linetype = 2, 
             color = "lightgray", alpha=0.5)
ggsave(p1, filename = "D:/R/hfp.pdf", width=6, height = 4)
#########################################




