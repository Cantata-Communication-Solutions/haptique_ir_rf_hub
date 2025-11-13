"""Haptique IR/RF hub integration for Home Assistant."""
import logging
import asyncio
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BUTTON, Platform.SENSOR, Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Haptique IR/RF hub from a config entry."""
    host = entry.data[CONF_HOST]
    token = entry.data.get(CONF_TOKEN, "")
    
    # Create API client
    session = async_get_clientsession(hass)
    api = HaptiqueGatewayAPI(host, token, session)
    
    # Test connection
    try:
        await api.get_status()
    except Exception as err:
        _LOGGER.error("Failed to connect to  Haptique IR/RF hub: %s", err)
        return False
    
    # Create coordinator for updates
    coordinator = HaptiqueDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    await async_setup_services(hass, api)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_setup_services(hass: HomeAssistant, api) -> None:
    """Set up services for Haptique IR/RF hub."""
    
    async def send_rf_code(call):
        """Send RF code service."""
        code = call.data.get("code")
        bits = call.data.get("bits", 24)
        protocol = call.data.get("protocol", 1)
        repeat = call.data.get("repeat", 8)
        
        await api.send_rf_code(code, bits, protocol, repeat)
    
    async def send_rf_saved(call):
        """Send saved RF command service."""
        name = call.data.get("name")
        await api.send_rf_saved(name)
    
    async def send_ir_code(call):
        """Send IR code service."""
        freq = call.data.get("frequency", 38000)
        duty = call.data.get("duty", 33)
        raw_data = call.data.get("raw_data", [])
        
        await api.send_ir_code(freq, duty, raw_data)
    
    async def send_ir_saved(call):
        """Send saved IR command service."""
        name = call.data.get("name")
        await api.send_ir_saved(name)
    
    async def save_rf_last(call):
        """Save last received RF command."""
        name = call.data.get("name")
        await api.save_rf_command(name)
    
    async def save_ir_last(call):
        """Save last received IR command."""
        name = call.data.get("name")
        await api.save_ir_command(name)
    
    async def delete_rf_command(call):
        """Delete saved RF command."""
        name = call.data.get("name")
        await api.delete_rf_command(name)
    
    async def delete_ir_command(call):
        """Delete saved IR command."""
        name = call.data.get("name")
        await api.delete_ir_command(name)
    
    # Register all services
    hass.services.async_register(DOMAIN, "send_rf_code", send_rf_code)
    hass.services.async_register(DOMAIN, "send_rf_saved", send_rf_saved)
    hass.services.async_register(DOMAIN, "send_ir_code", send_ir_code)
    hass.services.async_register(DOMAIN, "send_ir_saved", send_ir_saved)
    hass.services.async_register(DOMAIN, "save_rf_last", save_rf_last)
    hass.services.async_register(DOMAIN, "save_ir_last", save_ir_last)
    hass.services.async_register(DOMAIN, "delete_rf_command", delete_rf_command)
    hass.services.async_register(DOMAIN, "delete_ir_command", delete_ir_command)


class HaptiqueDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Haptique IR/RF hub data."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(10):
                status = await self.api.get_status()
                rf_status = await self.api.get_rf_status()
                rf_saved = await self.api.get_rf_saved()
                ir_saved = await self.api.get_ir_saved()
                
                return {
                    "status": status,
                    "rf_status": rf_status,
                    "rf_saved": rf_saved,
                    "ir_saved": ir_saved,
                }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}")


class HaptiqueGatewayAPI:
    """API client for Haptique IR/RF hub."""

    def __init__(self, host: str, token: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.host = host
        self.token = token
        self.session = session
        self.base_url = f"http://{host}"
        
    def _get_headers(self) -> dict:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make API request with authentication."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            async with async_timeout.timeout(10):
                async with self.session.request(
                    method, url, headers=headers, **kwargs
                ) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout connecting to {url}") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error connecting to {url}: {err}") from err
    
    async def get_status(self) -> dict:
        """Get device status."""
        return await self._request("GET", "/api/status")
    
    async def get_rf_status(self) -> dict:
        """Get RF status."""
        return await self._request("GET", "/api/rf/status")
    
    async def get_rf_saved(self) -> list:
        """Get saved RF commands."""
        result = await self._request("GET", "/api/rf/saved")
        return result.get("commands", [])
    
    async def get_ir_saved(self) -> list:
        """Get saved IR commands."""
        result = await self._request("GET", "/api/ir/saved")
        return result.get("commands", [])
    
    async def send_rf_code(self, code: int, bits: int, protocol: int, repeat: int) -> dict:
        """Send RF code."""
        return await self._request(
            "POST",
            "/api/rf/send",
            json={
                "code": code,
                "bits": bits,
                "protocol": protocol,
                "repeat": repeat
            }
        )
    
    async def send_rf_saved(self, name: str) -> dict:
        """Send saved RF command."""
        return await self._request("POST", "/api/rf/send/name", json={"name": name})
    
    async def send_ir_code(self, freq: int, duty: int, raw_data: list) -> dict:
        """Send IR code."""
        return await self._request(
            "POST",
            "/api/ir/send",
            json={
                "freq": freq,
                "duty": duty,
                "raw": raw_data
            }
        )
    
    async def send_ir_saved(self, name: str) -> dict:
        """Send saved IR command."""
        return await self._request("POST", "/api/ir/send/name", json={"name": name})
    
    async def save_rf_command(self, name: str) -> dict:
        """Save last received RF command."""
        return await self._request("POST", "/api/rf/save", json={"name": name})
    
    async def save_ir_command(self, name: str) -> dict:
        """Save last received IR command."""
        return await self._request("POST", "/api/ir/save", json={"name": name})
    
    async def delete_rf_command(self, name: str) -> dict:
        """Delete saved RF command."""
        return await self._request("DELETE", "/api/rf/delete", json={"name": name})
    
    async def delete_ir_command(self, name: str) -> dict:
        """Delete saved IR command."""
        return await self._request("DELETE", "/api/ir/delete", json={"name": name})
