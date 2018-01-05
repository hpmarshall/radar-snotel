#!/bin/bash
cd /Users/hpm/D_DRIVE/CryoToolbox/WINTER2017-18/CODE/
rsync -vaurP -e ssh radar@ipcflows.cloudapp.net:SatFrom/ /Users/hpm/D_DRIVE/CryoToolbox/WINTER2017-18/SATDATA/
source /Users/hpm/anaconda/envs/obsio_env/bin/activate obsio_env && pythonw /Users/hpm/D_DRIVE/CryoToolbox/WINTER2017-18/CODE/readFEradarSat2.py
pythonw /Users/hpm/D_DRIVE/CryoToolbox/WINTER2017-18/CODE/readFEradarSat2_Bogus.py
scp BannerSWEdar.png cgiss.boisestate.edu:public_html/login/
scp BogusSWEdar.png cgiss.boisestate.edu:public_html/login/
