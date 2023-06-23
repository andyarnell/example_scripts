##consolidating folders
#renaming main folder
file.rename("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/AOH_26092020", "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020") 
#deleting carbon files (still in raw)
folder_old_path =  "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/carbon_agbc"
unlink(x = folder_old_path, recursive = TRUE)
rm(folder_old_path)
##############
#unzipping sets folder for the ten subsets
folder_path =  "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020"
zipF<- paste0(folder_path,"/","sets.zip")
outDir<-paste0(folder_path,"/","sets")
unzip(zipF,exdir=outDir)

######## copy all files in folder_old_path to path_new
folder_old_path = "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/plantaeBGCI_10km"
path_new = "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/KEW_PLANTAE_BGCI_10km"
dir.create(path_new, showWarnings = TRUE)
current_files = list.files(folder_old_path, full.names = TRUE)
file.copy(from = current_files, to = path_new, recursive = FALSE, copy.mode = TRUE)
#delete old folder (check if works - may require permissions)
unlink(x = folder_old_path, recursive = TRUE)

####################### copy all files in folder_old_path to path_new 
folder_old_path = "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/reptiliaGARD_10km"
path_new = "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/GARDreptilia_10km"
current_files = list.files(folder_old_path, full.names = TRUE)
dir.create(path_new, showWarnings = TRUE)
file.copy(from = current_files, to = path_new, recursive = FALSE, copy.mode = TRUE)
#delete old folder (check if works - may require permissions)
unlink(x = folder_old_path, recursive = TRUE)

#####################
# folder_old_path = "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/sets/sets/_"
# path_new = "C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/sets/sets"
# current_files = list.files(folder_old_path, full.names = TRUE)
# file.copy(from = current_files, to = path_new, recursive = FALSE, copy.mode = TRUE)
# #delete old folder (check if works - may require permissions)
# unlink(x = folder_old_path, recursive = TRUE)

##############
##create output folder
dir.create(file.path("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020", "aoh_summing"), showWarnings = FALSE)
##create output subfolders
dir.create(file.path("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/aoh_summing", "all_sp_richness"), showWarnings = FALSE)
dir.create(file.path("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/aoh_summing", "thr_sp_richness"), showWarnings = FALSE)
dir.create(file.path("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/aoh_summing", "all_sp_rwr"), showWarnings = FALSE)
dir.create(file.path("C:/Users/andya/OneDrive - WCMC(1) (1)/Data/naturemap/working/aoh_richness_rwr_sept2020/aoh_summing", "thr_sp_rwr"), showWarnings = FALSE)

