Scripts by AA for sept 2020 nature map runs
used folder prep r script to clean the data.

based on scripts 0 to 5: 
previously found here O:\01_projects_active\Global\p08425_naturemap\scripts_tools\)
and input lists of sets of species along with the AOH maps and the feature_data_list.rds

Scripts:
path to data may need changing to O drive data:
O:\f01_projects_active\Global\p08425_naturemap\work_in_progress\IUCN_2019_2_processing\september2020\aoh_richness_rwr_sept2020)

script 0 
makes feature_data_list.rds into a csv. It also makes a threatened feature list csv by -
selecting CR, EN and VU species from the IUCN status category (excl GARD reptiles which dont have threatened species data)
and combines this list with those plants listed as threatened csv from Malin and makes - 
a combined list of all threatened species. 
This list is later used to filter species for threatened sp richness subsets.

script 1 
walks through and lists all file names for the tifs and the paths

script 2 
combines info from column names and other aspects and merge/join to -
original 10 csvs of sets of species, then make new sets of species lists as csvs with filenames.

scripts 3a and 3b 
then use the output csv to make richness and RWR respectively.

Make sure to not rerun 3a and 3b scripts and attempt to overwrite, 
as seem to get an artifact - getting double counts - for first subset at least.
So rerun outputs somewhere else (an empty folder) if redoing the processing.


