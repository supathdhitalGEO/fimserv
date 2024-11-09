import os
import re
import requests
import pandas as pd
from pathlib import Path
import netCDF4 as nc
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from ..datadownload import setup_directories


# Downloading the short range forecast data
def download_nc_files(date_str, current_hour, download_dir, url_base, forecast_range):
    forecast_type = re.sub(
        r"(?i)shortrange|short[-\s]?range", "short_range", forecast_range
    )
    forecast_type = re.sub(
        r"(?i)mediumrange|medium[-\s]?range", "medium_range-mem1", forecast_type
    )
    forecast_type = re.sub(
        r"(?i)longrange|long[-\s]?range", "long_range_mem1", forecast_type
    )

    url = f"{url_base}/nwm.{date_str}/{forecast_type}/"

    date_output_dir = os.path.join(download_dir, "netCDF", date_str)
    os.makedirs(date_output_dir, exist_ok=True)

    # Define the pattern dynamically using current_hour for matching files
    if forecast_type == "short_range":
        pattern = (
            rf"nwm\.t{current_hour:02d}z\.short_range\.channel_rt\.f\d{{3}}\.conus\.nc"
        )
    elif forecast_type == "medium_range_mem1":
        pattern = rf"nwm\.t{current_hour:02d}z\.medium_range\.channel_rt_1\.f\d{{3}}\.conus\.nc"
    elif forecast_type == "long_range_mem1":
        pattern = (
            rf"nwm\.t{current_hour:02d}z\.long_range\.channel_rt_1\.f\d{{3}}\.conus\.nc"
        )

    # Fetch webpage content and look for files matching the pattern
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    nc_files = [
        link["href"]
        for link in soup.find_all("a", href=True)
        if re.search(pattern, link["href"])
    ]

    if not nc_files:
        return False, date_output_dir

    # Create a subfolder for each forecast hour
    hour_output_dir = os.path.join(date_output_dir, f"{current_hour:02d}")
    os.makedirs(hour_output_dir, exist_ok=True)

    for nc_file in nc_files:
        file_url = url + nc_file
        file_path = os.path.join(hour_output_dir, nc_file)
        file_response = requests.get(file_url)
        with open(file_path, "wb") as f:
            f.write(file_response.content)
    return True, hour_output_dir


# %%
# Process netcf and get the file in CSV format and extract all feature_is's discharge data
def process_netcdf_file(netcdf_file_path, filter_df, output_folder_path):
    base_filename = os.path.basename(netcdf_file_path).replace(".nc", "")
    output_csv_file_path = os.path.join(output_folder_path, f"{base_filename}.csv")

    try:
        ds = nc.Dataset(netcdf_file_path, "r")
        streamflow_data = ds.variables["streamflow"][:]
        feature_ids = ds.variables["feature_id"][:]
        ds.close()
    except Exception as e:
        print(f"Error reading NetCDF file {netcdf_file_path}: {e}")
        return

    if len(streamflow_data) == 0 or len(feature_ids) == 0:
        print(f"No data found in {netcdf_file_path}")
        return

    data_df = pd.DataFrame({"feature_id": feature_ids, "discharge": streamflow_data})

    filtered_df = data_df[data_df["feature_id"].isin(filter_df["feature_id"])]
    merged_df = pd.merge(filter_df[["feature_id"]], filtered_df, on="feature_id")
    merged_df.to_csv(output_csv_file_path, index=False)
    # print(f'Filtered DataFrame saved to {output_csv_file_path}')


# %%
def main(
    download_dir,
    output_csv_filename,
    HUC,
    data_dir,
    output_dir,
    forecast_range,
    sort_by="maximum",
    url_base="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/",
):

    # Step 2: Set up current date and hour to locate the latest forecast data
    today = datetime.utcnow().strftime("%Y%m%d")
    current_hour = datetime.utcnow().hour

    success = False
    attempts = 0

    # Step 3: Attempt to download data up to 24 times, checking back one hour at a time if needed
    while not success and attempts < 24:
        attempts += 1
        success, date_output_dir = download_nc_files(
            today, current_hour, download_dir, url_base, forecast_range
        )
        if not success:
            current_hour = (current_hour - 1) % 24
            if current_hour == 23:
                today = (datetime.utcnow() - timedelta(days=1)).strftime("%Y%m%d")

    if not success:
        print("No recent forecast data found. Exiting.")
        return

    # Step 4: Load the filter CSV containing the feature_ids of interest
    filter_csv_file_path = os.path.join(output_dir, output_csv_filename)
    output_folder_path = os.path.join(download_dir, "csvFiles")
    os.makedirs(output_folder_path, exist_ok=True)
    filter_df = pd.read_csv(filter_csv_file_path)

    # Step 5: Process each NetCDF file in the downloaded directory
    if os.path.exists(date_output_dir):
        for root, _, files in os.walk(date_output_dir):
            for filename in files:
                if filename.endswith(".nc"):
                    netcdf_file_path = os.path.join(root, filename)
                    process_netcdf_file(netcdf_file_path, filter_df, output_folder_path)

    # Step 6: Combine all processed CSVs into a single DataFrame
    csv_directory = output_folder_path
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]

    if not csv_files:
        print("No CSV files found after processing NetCDF files.")
        return

    combined_df = pd.concat(
        [
            pd.read_csv(os.path.join(csv_directory, file))[["feature_id", "discharge"]]
            for file in csv_files
        ]
    )

    # Step 7: Reformat the combined data to create a table of discharge values for each feature_id
    combined_df = (
        combined_df.pivot_table(index="feature_id", values="discharge", aggfunc=list)
        .apply(pd.Series.explode)
        .reset_index()
    )
    combined_df["discharge"] = combined_df["discharge"].astype(float)
    combined_df = (
        combined_df.groupby("feature_id")["discharge"].apply(list).reset_index()
    )

    # Step 8: Efficiently Separate discharge values into individual columns for easy analysis
    discharge_values = pd.DataFrame(
        combined_df["discharge"].tolist(), index=combined_df.index
    )
    discharge_values.columns = [
        f"discharge_{i+1}" for i in range(discharge_values.shape[1])
    ]

    # Concatenate the discharge columns to the original DataFrame and drop the 'discharge' column
    combined_df = pd.concat(
        [combined_df.drop(columns=["discharge"]), discharge_values], axis=1
    )
    output_file = os.path.join(download_dir, "combined_streamflow.csv")
    combined_df.to_csv(output_file, index=False)

    if sort_by == "minimum":
        discharge_stat_df = (
            combined_df.set_index("feature_id").min(axis=1).reset_index()
        )
    elif sort_by == "median":
        discharge_stat_df = (
            combined_df.set_index("feature_id").median(axis=1).reset_index()
        )
    else:
        discharge_stat_df = (
            combined_df.set_index("feature_id").max(axis=1).reset_index()
        )

    discharge_stat_df.columns = ["feature_id", "discharge"]
    output_file = os.path.join(data_dir, f"{forecast_range}_{HUC}.csv")
    discharge_stat_df.to_csv(output_file, index=False)
    print(f"The final discharge values saved to {output_file}")


# Short Range forecast URL
def getNWMForecasteddata(huc, forecast_range, sort_by="maximum"):
    code_dir, data_dir, output_dir = setup_directories()
    download_dir = os.path.join(
        output_dir, f"flood_{huc}", "discharge", f"{forecast_range}_forecast"
    )
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    featureIDs = Path(output_dir, f"flood_{huc}", "feature_IDs.csv")
    main(download_dir, featureIDs, huc, data_dir, output_dir, forecast_range, sort_by)
    print(f"Downloading NWM forecasted data for HUC {huc}...")
