import owphandfim as fm


huc = "03020202"

# Mention the data range  so that it will plot that specific range
start_date = "2020-01-01"
end_date = "2022-01-03"

feature_id = ["11239241", "11239079"]
# fm.getNWMretrospectivedata(start_date, end_date, huc)
fm.plotNWMStreamflow(huc, feature_id, start_date, end_date)

# To plot the USGS, First download the USGS site data for date range in sites
usgs_sites = ["02091814", "0209205053"]


# fm.getUSGSsitedata(start_date, end_date, usgs_sites, huc)
fm.plotUSGSStreamflow(huc, usgs_sites, start_date, end_date)

# To compare the discharge data between NWM and USGS
fm.CompareNWMnUSGSStreamflow(huc, feature_id[0], usgs_sites[0], start_date, end_date)

# to plot the SRC data user need the hydroID and corresponding branc ID
hydro_id = ["11640012", "11640001"]
branch_id = ["1097000033", "1097000033"]
dischargevalue = 200000

# User can pass the discharge value to get the stage value for that discharge
# fm.plotSRC(huc, hydro_id, branch_id)
