# Haptique IR/RF Hub Integration

## Overview

The Haptique IR/RF Hub integration allows you to control infrared (IR) and radio frequency (RF 433MHz) devices through Home Assistant using the Haptique IR/RF Hub hardware.

## Hardware

This integration works with:
- Kincony AG Hub with Haptique firmware
- ESP32-based IR/RF hubs running Haptique firmware

## Features

- Learn and replay IR commands
- Learn and replay RF (433MHz) commands  
- Store commands with custom names
- Local control (no cloud required)
- Web-based learning interface
- RESTful API control

## Configuration

### Prerequisites

1. Haptique IR/RF Hub device with firmware installed
2. Device connected to your network (2.4GHz WiFi)
3. Device IP address
4. Authentication token (from device configuration)

### Setup via UI

1. Navigate to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Haptique IR/RF Hub"**
4. Enter your device details:
   - **Host**: Device IP address (e.g., `192.168.1.100`)
   - **Token**: Authentication token from device
5. Click **Submit**

### Manual Configuration (YAML)
```yaml
# Not supported - use UI configuration
```

## Services

### `haptique_ir_rf_hub.send_ir`

Send an IR command.

**Service data:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of saved IR command |

**Example:**
```yaml
service: haptique_ir_rf_hub.send_ir_saved
data:
  name: "tv_power"
```

### `haptique_ir_rf_hub.send_rf`

Send an RF command.

**Service data:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of saved RF command |

**Example:**
```yaml
service: haptique_ir_rf_hub.send_rf_saved
data:
  name: "fan_on"
```

### `haptique_ir_rf_hub.save_ir_last`

Save the last received IR command.

**Service data:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name to save command as |
| `frame` | string | No | Frame type (default: "B") |

### `haptique_ir_rf_hub.save_rf_last`

Save the last received RF command.

**Service data:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name to save command as |

## Learning Commands

### IR Commands

1. Point IR remote at hub
2. Press button on remote
3. Call `save_ir_last` service with desired name
4. Command is now saved and ready to use

### RF Commands

1. Press button on RF remote (433MHz)
2. Call `save_rf_last` service with desired name
3. Command is now saved and ready to use

## Automation Examples

### Turn on TV at specific time
```yaml

  - alias: "Morning TV On"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: haptique_ir_rf_hub.send_ir_saved
        data:
          name: "tv_power"
```
### Turn on TV RAW code
```yaml
alias: TV ON RAW
description: ""
trigger:
  - platform: time
    at: "07:00:00"

action:
  - service: haptique_ir_rf_hub.send_ir_code
    data:
      frequency: 38000
      duty: 33
      raw_data:
        [4540,4495,573,1670,575,1671,574,1670,574,548,575,548,574,549,575,547,576,547,
         575,1670,576,1669,576,1669,576,546,576,547,576,547,577,545,577,546,576,547,
         576,1669,608,515,576,546,577,546,607,516,610,512,577,545,610,1636,607,515,
         577,1668,607,1638,609,1635,614,1631,610,1635,613,1632,614,300]

mode: single

```

## Troubleshooting

### Device Not Found

- Verify device is powered and connected to network
- Check IP address hasn't changed
- Ensure device and HA are on same network
- Try accessing device API directly: `http://<device-ip>/api/status`

### Commands Not Working

- Verify device has line of sight to controlled device
- Check device placement for optimal IR/RF range
- Ensure command was learned correctly
- Test command via device web interface first

### Authentication Errors

- Verify token is correct
- Re-obtain token from device configuration
- Check for special characters in token

## Technical Details

- **Integration Type**: Hub
- **IoT Class**: Local Polling
- **Config Flow**: Yes (UI configuration)
- **Protocols**: IR (38kHz), RF (433MHz)

## Limitations

- RF only supports 433MHz fixed code protocols
- Requires 2.4GHz WiFi (5GHz not supported)
- Local network access required
- Device must have static IP or DHCP reservation recommended

## Additional Resources

- [GitHub Repository](https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub)
- [Firmware Repository](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)
- [Issue Tracker](https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub/issues)
