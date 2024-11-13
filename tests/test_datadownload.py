import owphandfim as fm

huc = "03020202"


# Download the data
fm.DownloadHUC8(huc)

# If user wants to update the streamorder

stream_order = [6, 5]
# fm.DownloadHUC8(huc, stream_order)
