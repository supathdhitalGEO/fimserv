import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from teehr.loading.usgs.usgs import usgs_to_parquet

from ..datadownload import setup_directories


def getUSGSdata(data_dir, usgs_sites):
    location_id = f"usgs-{usgs_sites}"
    files = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(".parquet")
    ]
    all_data = pd.DataFrame()
    for file in files:
        df = pd.read_parquet(file)
        matched_rows = df[df["location_id"] == location_id]
        all_data = pd.concat([all_data, matched_rows])
    filtered_data = all_data[["value_time", "value"]]
    filtered_data.rename(
        columns={"value_time": "Date", "value": "Discharge"}, inplace=True
    )

    return filtered_data


def plotNWMStreamflowData(dischargedata, usgs_sites):
    plt.figure(figsize=(10, 5))

    # Loop through the list of feature_ids and plot each one
    for usgs_site in usgs_sites:
        data = getUSGSdata(dischargedata, usgs_site)
        plt.plot(
            data["Date"],
            data["Discharge"],
            label=f"USGS streamflow for gauge site: {usgs_site}",
            linewidth=2,
        )

    plt.xlabel("Date (Hourly)", fontsize=14)
    plt.ylabel("Discharge (m3/s)", fontsize=14)
    plt.title("USGS Streamflows", fontsize=16)
    plt.legend()
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which="both", linestyle="-", linewidth=0.3)
    plt.tight_layout()
    plt.show()


def getusgs_discharge(
    start_date,
    end_date,
    usgs_sites,
    output_root,
):
    output_dir = Path(output_root) / "discharge" / "usgs_streamflow"
    output_dir.mkdir(parents=True, exist_ok=True)

    usgs_to_parquet(
        start_date=start_date,
        end_date=end_date,
        sites=usgs_sites,
        output_parquet_dir=output_dir,
    )
    print(f"USGS discharge data saved to {output_dir}.")


def getUSGSsitedata(start_date, end_date, usgs_sites, huc):
    code_dir, data_dir, output_dir = setup_directories()

    HUC_dir = os.path.join(output_dir, f"flood_{huc}")
    getusgs_discharge(start_date, end_date, usgs_sites, HUC_dir)


def plotUSGSStreamflow(huc, usgs_sites):
    code_dir, data_dir, output_dir = setup_directories()
    discharge_dir = os.path.join(
        output_dir, f"flood_{huc}", "discharge", "usgs_streamflow"
    )
    plotNWMStreamflowData(discharge_dir, usgs_sites)
