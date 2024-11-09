# Operational Flood Inundation Mapping(FIM) for CONUS

[![Version](https://img.shields.io/github/v/release/sdmlua/OperationalOWPFIM)](https://github.com/sdmlua/OperationalOWPFIM/releases)
[![Issues](https://img.shields.io/github/issues/sdmlua/OperationalOWPFIM)](https://github.com/sdmlua/OperationalOWPFIM/issues)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://opensource.org/licenses/GPL-3.0)
![Views](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/sdmlua/OperationalOWPFIM&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=Views&edge_flat=false)



### **Flood Inundation Mapping as a Service**
| | |
| --- | --- |
| <a href="https://sdml.ua.edu"><img src="https://sdml.ua.edu/wp-content/uploads/2023/01/SDML_logo_Sq_grey.png" alt="SDML Logo" width="300"></a> | This repository presents a sophisticated and user friendly approach to generate Operational flood inundation map using NOAA_OWP Height Above Nearest Drainage (HAND) method-FIM model using National Water Model retrospective and forecasted streamflow data.It is developed under Surface Dynamics Modeling Lab (SDML). |




### **Background**
NOAA-Office of Water Predictions (OWP) use HAND FIM model for operational flood forecasting across CONUS (https://github.com/NOAA-OWP/inundation-mapping). It is a terrain based model that uses the Discharge and reach avergaed synthetic rating curves (SRCs) to generate the inundation and depth rasters at HUC-8 scale (Hydrologic Unit Code-8). The model is capable to produce flood maps less than a minute for all order streams within the watershed. The HUC-8 watersheds have catchment area more than 1000 sqkm , that makes this framework scalable and computationaly efficient. It is a fluvial flood model and doesnot have urban flood compponant.The last released version of the model is 4.5and has gone through significant improvements.The present notebook is user freindly and able to run the HAND FIM model from cloud and capable of running mutiple HUC-8s simulteniously.This model can run at any temporal resolution(hourly, daily, monthly etc).It uses the NHDPlus unique river identifiers and assign the streamflow for each of the segment. 

### **Package structures**

```bash
OperationalOWPFIM/
├── docs/(contain the code code usage))
├── data/
│   └── inputs/(NWM Discharge value will be saved here in a format of STH_HUC8code)
├── src/owphandfim/
│           ├── streamflowdata/
                ├── nwmretrospectivedata.py
                └── forecasteddata.py
│           ├── plots/ (Contains different plotting functionality)
            ├── FIMsubset/
                ├── xycoord.py
                └── shpsubset.py
            ├── datadownload.py (Includes all HUC8 raster things)
            ├── runFIM.py (OWPHAND model)
└── tests/(includes test cases for each functionality)
```
### **Usage**
To use this code, 

```bash
pip install owphandfim
```

Once it installed, import it like 
```bash
import owphandfim as fm

#to download HUC8
fm.DownloadHUC8(HUC)    #Like this it contains multiples functionality.
```
Then there are a lot of different modules, call it to work. For reference to run, [Here (docs/code_usage.ipynb)](./docs/code_usage.ipynb) is the sample usuage of this code and different functionality. 
 
### **Acknowledgements**
| | |
| --- | --- |
| ![alt text](https://ciroh.ua.edu/wp-content/uploads/2022/08/CIROHLogo_200x200.png) | Funding for this project was provided by the National Oceanic & Atmospheric Administration (NOAA), awarded to the Cooperative Institute for Research to Operations in Hydrology (CIROH) through the NOAA Cooperative Agreement with The University of Alabama (#Funding ID). |

