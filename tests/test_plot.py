import owphandfim as fm

huc = "03020202"
feature_id = ["11239241", "11239079"]
# fm.plotNWMStreamflow(huc, feature_id)

# To plot the USGS, First download the USGS site data for date range in sites
usgs_sites = ["02091814", "0209205053"]

start_date = "2019-01-01"
end_date = "2020-01-03"

# fm.getUSGSsitedata(start_date, end_date, usgs_sites, huc)
# fm.plotUSGSStreamflow(huc, usgs_sites)

# To compare the discharge data between NWM and USGS
# fm.CompareNWMnUSGSStreamflow(huc, feature_id[0], usgs_sites[0])

# to plot the SRC data user need the hydroID and corresponding branc ID
hydro_id = ["11640012", "11640001"]
branch_id = ["1097000033", "1097000033"]
dischargevalue = 200000

# User can pass the discharge value to get the stage value for that discharge
fm.plotSRC(huc, hydro_id, branch_id)
