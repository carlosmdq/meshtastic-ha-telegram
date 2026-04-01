# Meshtastic + Home Assistant + Telegram

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-red.svg)](README.es.md)

Full integration of a Meshtastic mesh network with Home Assistant and a Telegram bot for monitoring, two-way messaging, and automated alerts.

## Architecture

```
Meshtastic Node (TCP :4403)
    ├── TCP direct → Home Assistant (native HACS integration)
    │                  ├── meshtastic_message_log events
    │                  └── meshtastic.send_text action
    │
    └── MQTT (JSON) → Mosquitto (:1883)
                       └── Home Assistant (MQTT integration)

Home Assistant Automations:
    ├── DM received → Telegram (notification)
    ├── Webhook ← Telegram bot → Meshtastic (send)
    ├── Node offline → Telegram alert
    ├── Low battery → Telegram alert
    └── Gateway disconnected → Telegram alert

Telegram Bot:
    └── /mesh command → webhook HA → meshtastic.send_text
```

## Components

### Home Assistant (`homeassistant/`)

5 ready-to-use YAML automations for your `automations.yaml`:

| Automation | Function |
|-----------|----------|
| `mesh_dm_a_telegram` | Forwards Meshtastic DMs to Telegram |
| `mesh_enviar_desde_telegram` | Webhook that receives from Telegram and sends via Meshtastic |
| `mesh_heltec_offline` | Alert if a node stops reporting (>1h) |
| `mesh_heltec_bateria_baja` | Alert when battery <20% |
| `mesh_gateway_desconectado` | Alert if gateway loses connection (>10min) |

**HA Requirements:**
- [Meshtastic Integration](https://github.com/meshtastic/homeassistant) (HACS)
- `rest_command.telegram_notify` configured (see below)

### Mosquitto MQTT (`mosquitto/`)

Local MQTT broker with Docker Compose. The Meshtastic node publishes JSON messages here.

```bash
cd mosquitto
docker compose up -d
```

### Telegram Bot (`telegram-bot/`)

`/mesh` command to send messages from Telegram to the Meshtastic network:

```
/mesh Hello everyone          → public channel
/mesh @<node_id> Hello        → DM to specific node
```

## Setup

### 1. Mosquitto

```bash
cd mosquitto
docker compose up -d
```

### 2. Configure Meshtastic Node

Point the node's MQTT to your local broker:

```bash
# Using meshtastic CLI
pip install meshtastic
meshtastic --host <NODE_IP> --set mqtt.address <MOSQUITTO_IP>
meshtastic --host <NODE_IP> --set mqtt.json true
meshtastic --host <NODE_IP> --set mqtt.encryption_enabled false
```

Or from the Meshtastic app: Module Settings → MQTT → set broker address.

### 3. Home Assistant

1. Install Meshtastic integration via HACS
2. Configure TCP connection to the node (IP:4403)
3. Add `rest_command` in `configuration.yaml`:

```yaml
rest_command:
  telegram_notify:
    url: "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage"
    method: POST
    content_type: "application/json"
    payload: '{"chat_id": <YOUR_CHAT_ID>, "text": "{{ title }}\n{{ message }}", "parse_mode": "HTML"}'
```

4. Copy automations from `homeassistant/automations.yaml`
5. Replace `XXXX` and `NODEID` with your actual node IDs

### 4. Telegram Bot

Integrate `telegram-bot/mesh_command.py` into your bot. Adjust `HA_WEBHOOK_URL` to your Home Assistant IP.

## Important Notes

- **Exclusive TCP connection**: if HA is connected to the node via TCP, the Meshtastic mobile app CANNOT connect simultaneously. To use the app, temporarily disable the Meshtastic integration in HA.
- **MQTT topics**: the node publishes to `msh/AR/2/json/` (adjust region for your location).
- **Local webhook**: the `mesh_enviar_desde_telegram` automation uses `local_only: true` — the bot must run on the same network as HA.

## Documentation

- `docs/meshtastic-ha-telegram-guide.pdf` — complete guide with diagrams (English)
- `docs/meshtastic-ha-telegram-guia.pdf` — guía completa con diagramas (Spanish)

## Hardware Used

- **Fixed gateway**: Seeed XIAO ESP32-S3 (solar powered)
- **Mobile node**: Heltec V3

## License

MIT
