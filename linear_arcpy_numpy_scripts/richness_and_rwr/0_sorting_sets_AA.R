#install.packages("dplyr",dependencies = TRUE)
library(dplyr)
#C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/
  
#all species
feature_data_list <-readRDS("O:/f01_projects_active/Global/p08425_naturemap/work_in_progress/IUCN_2019_2_processing/september2020/aoh_richness_rwr_sept2020/feature_data_list.rds")
str(feature_data_list)

write.csv(feature_data_list,"O:/f01_projects_active/Global/p08425_naturemap/work_in_progress/IUCN_2019_2_processing/september2020/aoh_richness_rwr_sept2020/feature_data_list.csv",row.names = FALSE)
#setwd("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/aoh_richness_rwr/sets/sets")
# str(feature_data_list)

##threatened species
threatPlants <- read.csv("O:/f01_projects_active/Global/p08425_naturemap/raw_data/species/plants_BGCI/Data/ThreatenedPlants140120.csv")
str(threatPlants)
yField="TaxonName"
xField = "binomial"

# makeClean = function (string){
#   string<-trimws(string)
#   string<-gsub(" ","_",string)
#   string<-tolower(string)
# }
# 
# head(threatPlants[1])
# threatPlants[1] <- lapply(threatPlants[1], as.character)
# threatPlants$joinField<-makeClean(threatPlants[1])
# head(threatPlants)
#test<-filter(feature_data_list, category %in% c("CR", "EN","VU"))
#str(test)
newMergedDF<-merge(feature_data_list,threatPlants,by.x=xField,by.y=yField,all.x=TRUE)
str(newMergedDF)
newMergedDF_threat<-filter(newMergedDF,Threatened=="Threatened" | category %in% c("CR", "EN","VU"))
str(newMergedDF_threat)
write.csv(newMergedDF_threat,"O:/f01_projects_active/Global/p08425_naturemap/work_in_progress/IUCN_2019_2_processing/aoh_richness_rwr_sept2020/feature_data_list_threatened_plants_and_IUCN_Vert.csv",row.names = FALSE)
# setwd("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/aoh_richness_rwr/sets/sets")
# 
