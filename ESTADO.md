# Meshtastic — Estado del proyecto

## Nodos propios

| Nodo | Dispositivo | IP/Puerto | Node ID |
|------|------------|-----------|---------|
| **Carlosmdq fijo solar** | Seeed XIAO S3 | 192.168.1.171:4403 | 501743372 (`!1de7ff0c`) |
| **Carlosmdq movil** | — | — | 2661459028 |

- **206 nodos** en la red regional AR
- **110 device_trackers** en HA, 109 con GPS

## Integración con Home Assistant

### Conexión TCP directa

- HA conecta a `192.168.1.171:4403` vía integración Meshtastic nativa
- **Limitación**: la conexión TCP es exclusiva — si HA está conectado, la app Meshtastic móvil NO puede conectar simultáneamente
- **Workaround**: para usar la app, deshabilitar la integración Meshtastic en HA (disabled_by=user en config_entries + restart)
- **TCP proxy en Server 1 (puerto 4403)**: escucha pero NO funciona con la app porque no replica el handshake inicial del nodo

### MQTT local (Mosquitto)

- **Broker**: Mosquitto en Docker en Server 1 (192.168.1.65:1883), `allow_anonymous`
- El nodo publica a `msh/AR/2/json/` con JSON habilitado y encryption off
- El nodo apunta al Mosquitto local (antes usaba mqtt.meshtastic.org)
- HA lee mensajes via MQTT además de TCP

### Automatizaciones en HA

| Automatización | Función |
|---------------|---------|
| `mesh_dm_a_telegram` | Si llega un DM con `pki=true`, reenvía por Telegram via rest_command |
| `mesh_enviar_desde_telegram` | Webhook `mesh_send_from_telegram` (local only, sin auth) — recibe POST `{message, to?}` y ejecuta `meshtastic.send_text` |

## Integración con claude-bot (Telegram)

Comando `/mesh` en claude-bot:

```
/mesh texto                    → envía al canal público
/mesh @node_id texto           → envía DM al nodo
```

Llama al webhook de HA (`mesh_send_from_telegram`).

## Configuración MQTT del nodo

Para cambiar la config MQTT del nodo, usar el venv meshtastic CLI:

```bash
source /tmp/mesh-venv/bin/activate
meshtastic --host 192.168.1.171 --set mqtt.address 192.168.1.65
meshtastic --host 192.168.1.171 --set mqtt.json true
meshtastic --host 192.168.1.171 --set mqtt.encryption_enabled false
```

## Archivos

- **Guía completa PDF**: `meshtastic-ha-telegram-guia.pdf` (en esta carpeta)
- **Generador PDF**: `meshtastic-ha-telegram-guia.py` (en `intercambio/de-claude/`)

## Pendientes

| Tarea | Estado |
|-------|--------|
| Resolver mapa Meshtastic en dashboard (panel custom redirige a "red-mesh", no carga vista "mapa") | Pendiente |
