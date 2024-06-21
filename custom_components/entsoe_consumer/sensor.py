from __future__ import annotations
from .entsoe_class import Entsoe_Class

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

Entsoe = Entsoe_Class()
Entsoe.api_key = ''
Entsoe.country_code = 'NL'
Entsoe.timezone = 'Europe/Amsterdam'
Entsoe.supplier_costs = 0.04
Entsoe.energy_tax = 0.1088
Entsoe.vat = 21
result = Entsoe.update_prices_online()

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([ExampleSensor()])
    add_entities([TodayAveragePriceSensor()])
    add_entities([TodayHighPriceSensor()])
    add_entities([TodayLowPriceSensor()])


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


class TemplatePriceSensor(SensorEntity):
    
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL


class TodayAveragePriceSensor(TemplatePriceSensor):
    
    _attr_name = "Entsoe Today Average Price"

    def update(self) -> None:
        self._attr_native_value = Entsoe.today.average

class TodayHighPriceSensor(TemplatePriceSensor):
    
    _attr_name = "Entsoe Today Highest Price"

    def update(self) -> None:
        self._attr_native_value = Entsoe.today.high

class TodayLowPriceSensor(TemplatePriceSensor):
    
    _attr_name = "Entsoe Today Lowest Price"

    def update(self) -> None:
        self._attr_native_value = Entsoe.today.low
