#!/bin/bash
rsync -vaurP -e ssh radar@ipcflows.cloudapp.net:SatFrom/ /Users/hpm/D_DRIVE/CryoToolbox/RADAR-SNOTEL/SatFrom/
source /Users/hpm/anaconda/envs/obsio_env/bin/activate obsio_env && pythonw /Users/hpm/D_DRIVE/CryoToolbox/RADAR-SNOTEL/readFEradarSat2.py
pythonw /Users/hpm/D_DRIVE/CryoToolbox/RADAR-SNOTEL/readFEradarSat2_Bogus.py
scp /Users/hpm/D_DRIVE/CryoToolbox/RADAR-SNOTEL/BannerSWEdar.png cgiss.boisestate.edu:public_html/login/
scp /Users/hpm/D_DRIVE/CryoToolbox/RADAR-SNOTEL/BogusSWEdar.png cgiss.boisestate.edu:public_html/login/
