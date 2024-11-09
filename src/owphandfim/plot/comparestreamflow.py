import os
import matplotlib.pyplot as plt

from .nwmfid import getFIDdata
from .usgs import getUSGSdata
from ..datadownload import setup_directories

plt.rcParams["font.family"] = "Arial"
def plotcomparision(data_dir_nwm, data_dir_usgs, feature_id, usgs_site):
    nwm_data = getFIDdata(data_dir_nwm, feature_id)
    usgs_data = getUSGSdata(data_dir_usgs, usgs_site)
    
    plt.figure(figsize=(10, 5))
    # Plot NWM data with solid line
    plt.plot(nwm_data['Date'], nwm_data['Discharge'], label=f'NWM Streamflow for {feature_id}', linestyle='-', linewidth=2)
    
    # Plot USGS data with dashed line
    plt.plot(usgs_data['Date'], usgs_data['Discharge'], label=f'USGS Streamflow for {usgs_site}', linestyle='-.', linewidth=1.5)
    
    plt.xlabel('Date (Hourly)', fontsize=14)
    plt.ylabel('Discharge (m3/s)', fontsize=14)
    plt.title('Discharge Comparison: NWM vs USGS', fontsize=16)
    plt.legend()
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.grid(True, which='both', linestyle='-', linewidth=0.3)
    plt.show()

def CompareNWMnUSGSStreamflow(huc, feature_id, usgs_site):
    code_dir, data_dir, output_dir = setup_directories()
    discharge_dir_nwm = os.path.join(output_dir, f"flood_{huc}", 'discharge', 'nwm30_retrospective')
    discharge_dir_usgs = os.path.join(output_dir, f"flood_{huc}", 'discharge', 'usgs_streamflow')
    plotcomparision(discharge_dir_nwm, discharge_dir_usgs, feature_id, usgs_site)
