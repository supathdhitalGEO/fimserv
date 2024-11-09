import pandas as pd
import os
import matplotlib.pyplot as plt

from ..datadownload import setup_directories

plt.rcParams["font.family"] = "Arial"


def getFIDdata(data_dir, feature_id):
    location_id = f"nwm30-{feature_id}"
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


def plotNWMStreamflowData(dischargedata, feature_ids, output_dir):
    plt.figure(figsize=(10, 5))

    # Loop through the list of feature_ids and plot each one
    for feature_id in feature_ids:
        data = getFIDdata(dischargedata, feature_id)
        plt.plot(
            data["Date"],
            data["Discharge"],
            label=f"NWM streamflow for feature ID: {feature_id}",
            linewidth=2,
        )

    plt.xlabel("Date (Hourly)", fontsize=14)
    plt.ylabel("Discharge (m³/s)", fontsize=14)
    plt.title("NWM Streamflows", fontsize=16)
    plt.legend()
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which="both", linestyle="-", linewidth=0.3)
    plt.tight_layout()
    
    #Save dir
    plt_dir = os.path.join(output_dir, 'Plots')
    os.makedirs(plt_dir, exist_ok=True)
    plot_dir = os.path.join(plt_dir, f"NWMStreamflow_{feature_id}.png")
    plt.savefig(plot_dir, dpi = 500, bbox_inches = 'tight')
    plt.show()


# Main function to drive the process
def plotNWMStreamflow(huc, feature_ids):
    code_dir, data_dir, output_dir = setup_directories()
    huc_dir = os.path.join(output_dir, f"flood_{huc}")
    discharge_dir = os.path.join(
        output_dir, f"flood_{huc}", "discharge", "nwm30_retrospective"
    )
    plotNWMStreamflowData(discharge_dir, feature_ids, huc_dir)
