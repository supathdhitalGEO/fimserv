import os

import owphandfim as fm

huc = "03020202"

# mention the forecast range as shortrange or mediumrange or longrange
# Download the data
# fm.getNWMForecasteddata(huc, forecast_range='shortrange')

# By default the data will be filtered based on maximum discharge value
# Otherwise user need to mention

fm.getNWMForecasteddata(huc, forecast_range="shortrange", sort_by="maximum")
fm.getNWMForecasteddata(huc, forecast_range="longrange", sort_by="minimum")
