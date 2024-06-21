from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from entsoe_class import Entsoe_Class
import os
import pandas as pd

Entsoe = Entsoe_Class()

load_dotenv()
Entsoe.api_key = os.getenv('API_KEY')

Entsoe.country_code = 'NL'
# https://annualreport2016.entsoe.eu/members/

Entsoe.timezone = 'Europe/Amsterdam'

# ANWB Energy costs (Opslag) per kwh
Entsoe.supplier_costs = 0.04

# Dutch Energytax per kwh
Entsoe.energy_tax = 0.1088

# Dutch VAT (Omzetbelasting) in %
Entsoe.vat = 21

# Update The Class Object Parameters with new prices.
result = Entsoe.update_prices_online()

if result == 0:
    print ('No data returned')
elif result == 168:
    print ('Week retrieved, tomorrow unavailable')
elif result == 192:
    print ('Week retrieved including tomorrow')
else:
    print (f'Incomplete data retrieved, only {result} records, expecting 168 or 192')

print (Entsoe)
print ('----')


result = Entsoe.update_prices_offline()

if result == 0:
    print ('No enough offline data for update anything')
elif result == 1:
    print (f'We updated the current hour next hour prices')
elif result == 2:
    print ('Current Hour Updated, but not enough offline data for updating the next hour')
elif result == 3:
    print (f'We moved to the next day')
elif result < 192:
    print (f'Not enough offline data for moving to new day, only {result} records')

print (Entsoe)
print ('----')
