import pandas as pd
import os
import matplotlib.pyplot as plt

from ..datadownload import setup_directories

plt.rcParams["font.family"] = "Arial"


def getFIDdata(data_dir, feature_id, start_date, end_date):
    location_id = f"nwm30-{feature_id}"

    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    start_dateSTR = start_date.strftime("%Y%m%d")
    end_dateSTR = end_date.strftime("%Y%m%d")
    target_file = f"{start_dateSTR}_{end_dateSTR}.parquet"

    target_dir = os.path.join(data_dir, target_file)

    if not os.path.exists(target_dir):
        raise FileNotFoundError(
            f"No NWM data found for the date range: {target_file} in {data_dir}. "
            "Please check the date range that you downloaded for that HUC."
        )

    df = pd.read_parquet(target_dir)
    matched_rows = df[df["location_id"] == location_id]

    # Prepare the filtered data with desired columns
    filtered_data = matched_rows[["value_time", "value"]]
    filtered_data.rename(
        columns={"value_time": "Date", "value": "Discharge"}, inplace=True
    )

    return filtered_data


def plotNWMStreamflowData(dischargedata, feature_ids, output_dir, start_date, end_date):
    plt.figure(figsize=(10, 5))

    # Loop through the list of feature_ids and plot each one
    for feature_id in feature_ids:
        data = getFIDdata(dischargedata, feature_id, start_date, end_date)
        plt.plot(
            data["Date"],
            data["Discharge"],
            label=f"NWM streamflow for feature ID: {feature_id}",
            linewidth=2,
        )

    plt.xlabel("Date (Hourly)", fontsize=14)
    plt.ylabel("Discharge (m³/s)", fontsize=14)
    plt.title("NWM hourly streamflow", fontsize=16)
    plt.legend()
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which="both", linestyle="-", linewidth=0.3)
    plt.tight_layout()

    # Save dir
    plt_dir = os.path.join(output_dir, "Plots")
    os.makedirs(plt_dir, exist_ok=True)
    plot_dir = os.path.join(plt_dir, f"NWMStreamflow_{feature_id}.png")
    plt.savefig(plot_dir, dpi=500, bbox_inches="tight")
    plt.show()


# Main function to drive the process
def plotNWMStreamflow(huc, feature_ids, start_date, end_date):
    code_dir, data_dir, output_dir = setup_directories()
    huc_dir = os.path.join(output_dir, f"flood_{huc}")
    discharge_dir = os.path.join(
        output_dir, f"flood_{huc}", "discharge", "nwm30_retrospective"
    )
    plotNWMStreamflowData(discharge_dir, feature_ids, huc_dir, start_date, end_date)
