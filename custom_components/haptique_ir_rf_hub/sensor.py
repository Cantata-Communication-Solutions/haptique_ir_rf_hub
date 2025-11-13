"""Sensor platform for Haptique IR/RF hub."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Haptique IR/RF hub sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    sensors = [
        HaptiqueWifiStatusSensor(coordinator, entry),
        HaptiqueRfCountSensor(coordinator, entry),
        HaptiqueVersionSensor(coordinator, entry),
        HaptiqueHostnameSensor(coordinator, entry),
        HaptiqueIpAddressSensor(coordinator, entry),
    ]
    
    async_add_entities(sensors)


class HaptiqueBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Haptique sensors."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version=coordinator.data.get("status", {}).get("version", "Unknown"),
        )


class HaptiqueWifiStatusSensor(HaptiqueBaseSensor):
    """WiFi status sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "WiFi Status"
        self._attr_unique_id = f"{entry.entry_id}_wifi_status"
        self._attr_icon = "mdi:wifi"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        status = self.coordinator.data.get("status", {})
        wifi_status = status.get("wifi_status", "unknown")
        
        if wifi_status == 3:
            return "Connected"
        elif wifi_status == 6:
            return "Disconnected"
        else:
            return f"Status {wifi_status}"

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        status = self.coordinator.data.get("status", {})
        return {
            "ssid": status.get("ssid", "N/A"),
            "rssi": status.get("rssi", 0),
            "local_ip": status.get("local_ip", "N/A"),
        }


class HaptiqueRfCountSensor(HaptiqueBaseSensor):
    """RF receive count sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "RF Received Count"
        self._attr_unique_id = f"{entry.entry_id}_rf_count"
        self._attr_icon = "mdi:radio-tower"
        self._attr_native_unit_of_measurement = "signals"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        rf_status = self.coordinator.data.get("rf_status", {})
        return rf_status.get("rx_count", 0)

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        rf_status = self.coordinator.data.get("rf_status", {})
        return {
            "last_code": rf_status.get("last_code", 0),
            "last_bits": rf_status.get("last_bits", 0),
            "last_protocol": rf_status.get("last_protocol", 0),
            "rf_rx_pin": rf_status.get("rf_rx_pin", 0),
            "rf_tx_pin": rf_status.get("rf_tx_pin", 0),
        }


class HaptiqueVersionSensor(HaptiqueBaseSensor):
    """Firmware version sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Firmware Version"
        self._attr_unique_id = f"{entry.entry_id}_version"
        self._attr_icon = "mdi:chip"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        status = self.coordinator.data.get("status", {})
        return status.get("version", "Unknown")


class HaptiqueHostnameSensor(HaptiqueBaseSensor):
    """Hostname sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Hostname"
        self._attr_unique_id = f"{entry.entry_id}_hostname"
        self._attr_icon = "mdi:network"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        status = self.coordinator.data.get("status", {})
        return status.get("hostname", "Unknown")


class HaptiqueIpAddressSensor(HaptiqueBaseSensor):
    """IP Address sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "IP Address"
        self._attr_unique_id = f"{entry.entry_id}_ip"
        self._attr_icon = "mdi:ip-network"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        status = self.coordinator.data.get("status", {})
        return status.get("local_ip", "N/A")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        status = self.coordinator.data.get("status", {})
        return {
            "mac": status.get("mac", "N/A"),
            "gateway": status.get("gateway", "N/A"),
        }
