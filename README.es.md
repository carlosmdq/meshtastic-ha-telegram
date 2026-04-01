# Meshtastic + Home Assistant + Telegram

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-red.svg)](README.es.md)

Integración completa de una red Meshtastic con Home Assistant y Telegram para monitoreo, mensajería bidireccional y alertas automáticas.

## Arquitectura

```
Meshtastic Node (TCP :4403)
    ├── TCP directo → Home Assistant (integración nativa HACS)
    │                  ├── Eventos meshtastic_message_log
    │                  └── Acción meshtastic.send_text
    │
    └── MQTT (JSON) → Mosquitto (:1883)
                       └── Home Assistant (integración MQTT)

Home Assistant Automations:
    ├── DM recibido → Telegram (notificación)
    ├── Webhook ← Telegram bot → Meshtastic (envío)
    ├── Nodo offline → alerta Telegram
    ├── Batería baja → alerta Telegram
    └── Gateway desconectado → alerta Telegram

Telegram Bot:
    └── /mesh comando → webhook HA → meshtastic.send_text
```

## Componentes

### Home Assistant (`homeassistant/`)

5 automatizaciones YAML listas para copiar a tu `automations.yaml`:

| Automatización | Función |
|---------------|---------|
| `mesh_dm_a_telegram` | Reenvía DMs de Meshtastic a Telegram |
| `mesh_enviar_desde_telegram` | Webhook que recibe de Telegram y envía por Meshtastic |
| `mesh_heltec_offline` | Alerta si un nodo deja de reportar (>1h) |
| `mesh_heltec_bateria_baja` | Alerta batería <20% |
| `mesh_gateway_desconectado` | Alerta si el gateway pierde conexión (>10min) |

**Requisitos HA:**
- [Integración Meshtastic](https://github.com/meshtastic/homeassistant) (HACS)
- `rest_command.telegram_notify` configurado (ver abajo)

### Mosquitto MQTT (`mosquitto/`)

Broker MQTT local con Docker Compose. El nodo Meshtastic publica mensajes JSON aquí.

```bash
cd mosquitto
docker compose up -d
```

### Bot Telegram (`telegram-bot/`)

Comando `/mesh` para enviar mensajes desde Telegram a la red Meshtastic:

```
/mesh Hola a todos          → canal público
/mesh @<node_id> Hola       → DM a nodo específico
```

## Setup

### 1. Mosquitto

```bash
cd mosquitto
docker compose up -d
```

### 2. Configurar nodo Meshtastic

Apuntar MQTT del nodo al broker local:

```bash
# Con meshtastic CLI
pip install meshtastic
meshtastic --host <IP_NODO> --set mqtt.address <IP_MOSQUITTO>
meshtastic --host <IP_NODO> --set mqtt.json true
meshtastic --host <IP_NODO> --set mqtt.encryption_enabled false
```

O desde la app Meshtastic: Module Settings → MQTT → configurar dirección del broker.

### 3. Home Assistant

1. Instalar integración Meshtastic via HACS
2. Configurar conexión TCP al nodo (IP:4403)
3. Agregar `rest_command` en `configuration.yaml`:

```yaml
rest_command:
  telegram_notify:
    url: "https://api.telegram.org/bot<TU_TOKEN>/sendMessage"
    method: POST
    content_type: "application/json"
    payload: '{"chat_id": <TU_CHAT_ID>, "text": "{{ title }}\n{{ message }}", "parse_mode": "HTML"}'
```

4. Copiar automatizaciones de `homeassistant/automations.yaml`
5. Reemplazar `XXXX` y `NODEID` con los IDs de tus nodos

### 4. Bot Telegram

Integrar `telegram-bot/mesh_command.py` en tu bot. Ajustar `HA_WEBHOOK_URL` a la IP de tu Home Assistant.

## Notas importantes

- **Conexión TCP exclusiva**: si HA está conectado al nodo por TCP, la app Meshtastic móvil NO puede conectar simultáneamente. Para usar la app, deshabilitar temporalmente la integración en HA.
- **MQTT topics**: el nodo publica en `msh/AR/2/json/` (ajustar región según tu ubicación).
- **Webhook local**: la automatización `mesh_enviar_desde_telegram` usa `local_only: true` — el bot debe correr en la misma red que HA.

## Documentación

- `docs/meshtastic-ha-telegram-guide.pdf` — complete guide with diagrams (English)
- `docs/meshtastic-ha-telegram-guia.pdf` — guía completa con diagramas (Español)

## Hardware usado

- **Gateway fijo**: Seeed XIAO ESP32-S3 (solar)
- **Nodo móvil**: Heltec V3

## Licencia

MIT
