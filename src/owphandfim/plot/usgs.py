import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from teehr.loading.usgs.usgs import usgs_to_parquet

from ..datadownload import setup_directories


def getUSGSdata(data_dir, usgs_sites, start_date, end_date):
    location_id = f"usgs-{usgs_sites}"

    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    start_dateSTR = start_date.strftime("%Y-%m-%d")
    end_dateSTR = end_date.strftime("%Y-%m-%d")
    target_file = f"{start_dateSTR}_{end_dateSTR}.parquet"

    target_dir = os.path.join(data_dir, target_file)

    if not os.path.exists(target_dir):
        raise FileNotFoundError(
            f"No USGS streamflow data found for the date range: {target_file} in {data_dir}. "
            "Please check the date range that you downloaded for that HUC."
        )

    df = pd.read_parquet(target_dir)
    matched_rows = df[df["location_id"] == location_id]

    filtered_data = matched_rows[["value_time", "value"]]
    filtered_data.rename(
        columns={"value_time": "Date", "value": "Discharge"}, inplace=True
    )
    return filtered_data


def plotNWMStreamflowData(dischargedata, usgs_sites, output_dir, start_date, end_date):
    plt.figure(figsize=(10, 5))

    # Loop through the list of feature_ids and plot each one
    for usgs_site in usgs_sites:
        data = getUSGSdata(dischargedata, usgs_site, start_date, end_date)
        plt.plot(
            data["Date"],
            data["Discharge"],
            label=f"USGS streamflow for gauge site: {usgs_site}",
            linewidth=2,
        )

    plt.xlabel("Date (Hourly)", fontsize=14)
    plt.ylabel("Discharge (m³/s)", fontsize=14)
    plt.title("USGS Streamflows", fontsize=16)
    plt.legend()
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which="both", linestyle="-", linewidth=0.3)
    plt.tight_layout()
    # Save dir
    plt_dir = os.path.join(output_dir, "Plots")
    os.makedirs(plt_dir, exist_ok=True)
    plot_dir = os.path.join(plt_dir, f"USGSStreamflow_{usgs_site}.png")
    plt.savefig(plot_dir, dpi=500, bbox_inches="tight")
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


def plotUSGSStreamflow(huc, usgs_sites, start_date, end_date):
    code_dir, data_dir, output_dir = setup_directories()
    discharge_dir = os.path.join(
        output_dir, f"flood_{huc}", "discharge", "usgs_streamflow"
    )
    HUC_dir = os.path.join(output_dir, f"flood_{huc}")
    plotNWMStreamflowData(discharge_dir, usgs_sites, HUC_dir, start_date, end_date)
