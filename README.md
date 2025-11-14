# Haptique IR/RF Hub - Home Assistant Integration

Control your IR (Infrared) and RF (433MHz) devices through Home Assistant with the Haptique IR/RF Hub.

## 📋 Overview

This custom integration allows you to learn and replay IR and RF commands using your Haptique IR/RF Hub device. Once configured, you can control your appliances, lights, fans, and other IR/RF devices directly from Home Assistant.

## ✨ Features

- **Learn IR Commands**: Capture infrared remote control signals
- **Learn RF Commands**: Capture 433MHz radio frequency signals
- **Store Commands**: All learned commands are stored in the Hub device
- **Home Assistant Integration**: Use learned commands as entities in automations
- **Easy Management**: Simple Lovelace card interface for learning new commands

## 📦 Prerequisites

- Home Assistant installed and running
- Haptique IR/RF Hub device
- Haptique Config App (to obtain device IP and Token)
- HACS (Home Assistant Community Store) installed

## 🚀 Installation

### Step 1: Install HACS

If you haven't already installed HACS, follow the instructions at [https://hacs.xyz/docs/setup/download](https://hacs.xyz/docs/setup/download)

### Step 2: Add Custom Repository

1. Open Home Assistant
2. Go to **HACS** > **Integrations**
3. Click the **three dots** menu in the top right corner
4. Select **Custom repositories**
5. Add the following repository URL:
   ```
   https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub
   ```
6. Select **Integration** as the category
7. Click **Add**

### Step 3: Install the Integration

1. In HACS, search for **"Haptique IR/RF Hub"**
2. Click on it and select **Download**
3. Restart Home Assistant

### Step 4: Add the Device in Haptique Config App

Before adding the integration to Home Assistant, ensure your Haptique IR/RF Hub is set up in the **Haptique Config App**. Note down the following details:
- Device IP Address
- Device Token

### Step 5: Configure in Home Assistant

1. Go to **Settings** > **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Haptique IR/RF Hub"**
4. Enter your device details:
   - **Device IP**: The IP address from Haptique Config App
   - **Token**: The authentication token from Haptique Config App
5. Click **Submit**

## 🎓 Learning Commands

### Setup Learning Interface

#### 1. Create Lovelace Card

Add the following card to your Lovelace dashboard:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 📚 Learn Commands
      Steps:
      1. Point remote at HUB  
      2. Press button  
      3. Type name  
      4. Toggle switch  
  - type: entities
    title: RF Command (433MHz)
    entities:
      - input_text.rf_command_name
      - input_boolean.save_rf_trigger
  - type: entities
    title: IR Command (Infrared)
    entities:
      - input_text.ir_command_name
      - input_boolean.save_ir_trigger
```

#### 2. Add Configuration

Add the following to your `configuration.yaml` file:

```yaml
input_text:
  rf_command_name:
    name: "RF Command Name"
    max: 50
  ir_command_name:
    name: "IR Command Name"
    max: 50

input_boolean:
  save_rf_trigger:
    name: "Save RF Trigger"
    icon: mdi:content-save
  save_ir_trigger:
    name: "Save IR Trigger"
    icon: mdi:content-save

automation:
  - alias: "Save RF Command"
    mode: single
    trigger:
      - platform: state
        entity_id: input_boolean.save_rf_trigger
        to: "on"
    condition:
      - condition: template
        value_template: "{{ states('input_text.rf_command_name') | length > 0 }}"
    action:
      - service: haptique_ir_rf_hub.save_rf_last
        data:
          name: "{{ states('input_text.rf_command_name') }}"
      - delay: "00:00:00.5"
      - service: persistent_notification.create
        data:
          title: "✅ RF Saved"
          message: "Command saved!"
      - service: input_text.set_value
        data:
          entity_id: input_text.rf_command_name
          value: ""
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.save_rf_trigger

  - alias: "Save IR Command"
    mode: single
    trigger:
      - platform: state
        entity_id: input_boolean.save_ir_trigger
        to: "on"
    condition:
      - condition: template
        value_template: "{{ states('input_text.ir_command_name') | length > 0 }}"
    action:
      - service: haptique_ir_rf_hub.save_ir_last
        data:
          name: "{{ states('input_text.ir_command_name') }}"
          frame: "B"
      - delay: "00:00:00.5"
      - service: persistent_notification.create
        data:
          title: "✅ IR Saved"
          message: "Command saved!"
      - service: input_text.set_value
        data:
          entity_id: input_text.ir_command_name
          value: ""
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.save_ir_trigger
```

**Important**: After adding this configuration, restart Home Assistant for the changes to take effect.

### How to Learn Commands

#### Learning IR Commands (Infrared)

1. Point your infrared remote at the Haptique Hub
2. Press the button you want to learn
3. In the Lovelace card, enter a name in **"IR Command Name"** field
4. Toggle the **"Save IR Trigger"** switch
5. Wait for the confirmation notification
6. The command is now saved and ready to use

#### Learning RF Commands (433MHz)

1. Point your RF remote at the Haptique Hub
2. Press the button you want to learn
3. In the Lovelace card, enter a name in **"RF Command Name"** field
4. Toggle the **"Save RF Trigger"** switch
5. Wait for the confirmation notification
6. The command is now saved and ready to use

## 💡 Using Learned Commands

Once commands are learned and saved in the Hub, you can use them in multiple ways:

### As Automation Actions

```yaml
automation:
  - alias: "Turn on TV"
    trigger:
      - platform: time
        at: "19:00:00"
    action:
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "tv_power"
```

### As Button Entities

Learned commands appear as entities in Home Assistant and can be added to your dashboard as buttons or used in scripts.

### In Scripts

```yaml
script:
  movie_mode:
    sequence:
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "tv_power"
      - delay: "00:00:02"
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "tv_hdmi_1"
```

## 🔧 Troubleshooting

### Device Not Found
- Ensure the Haptique Hub is powered on and connected to your network
- Verify the IP address hasn't changed (consider setting a static IP)
- Check that the device is added in the Haptique Config App

### Commands Not Learning
- Make sure you're pointing the remote directly at the Hub
- Ensure you enter a command name before toggling the save switch
- Check that the Hub is in learning mode (indicated by LED status)

### Token Issues
- Re-obtain the token from the Haptique Config App
- Remove and re-add the integration with the new token

## 📝 Support

For issues, questions, or feature requests, please open an issue on [GitHub](https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub/issues).

## 📄 License

This project is licensed under the MIT License - [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🙏 Credits

Developed by Cantata Communication Solutions
