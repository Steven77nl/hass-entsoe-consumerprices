from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from entsoe_class import Entsoe_Class
from pprint import pformat
import logging
import os
import pandas as pd


from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


'''
    _LOGGER = logging.getLogger("entsoe_consumer")
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    c_handler.setFormatter(c_format)
    _LOGGER.addHandler(c_handler)
    _LOGGER.setLevel(logging.INFO)
'''

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([ExampleSensor()])


class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 23




'''

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

#_LOGGER.warning('test')
#_LOGGER.info(Entsoe)


if result == 0:
    print ('No data returned')
elif result == 168:
    print ('Week retrieved, tomorrow unavailable')
elif result == 192:
    print ('Week retrieved including tomorrow')
else:
    print (f'Incomplete data retrieved, only {result} records, expecting 168 or 192')

print (result, Entsoe.currenthour, Entsoe.nexthour)
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

print (result, Entsoe.currenthour, Entsoe.nexthour)
print ('----')

'''