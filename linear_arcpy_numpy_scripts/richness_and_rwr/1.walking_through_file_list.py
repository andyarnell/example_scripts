##aim: 
##created by Andy Arnell 21/02/2020
##walk through all of the rawFolder directory, including subfolders and get: 
## 1) full path(fullPath), 2) filenames(filename), and 3) their directories (root)
##and put these as columns in a csv.
##an optional "endwith" can be for filtering can e used to select a certain type of file

print ("Importing packages")

import os
import pandas as pd

tempFolder = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020\aoh_summing" 
rawFolder = r"C:\Users\andya\OneDrive - WCMC(1) (1)\Data\naturemap\working\aoh_richness_rwr_sept2020"
extension = '.tif'

from os import walk

path = rawFolder

rootList = []
filenameList = []
fullPathList = []
for root, directories, filenames in os.walk(path):
##     for directory in directories:
##             print (os.path.join(root, directory) )
     for filename in filenames:
          if filename.endswith(".tif"):#select only tifs
              fullPathList.append(os.path.join(root,filename))
              filenameList.append(filename)
              rootList.append(root)


#rList = pd.DataFrame(rasterList,columns =['file_path'])
rList = pd.DataFrame(list(zip(fullPathList,rootList,filenameList)),columns =['fullPath','root','filename'])

rList = rList.drop(rList[rList.filename =="globalgrid_mollweide_10km.tif"].index)##drop/remove row for unwanted tif
#pd.write.csv(
print(rList.head())

rList.to_csv(os.path.join(tempFolder,"filenames.csv"))

             
