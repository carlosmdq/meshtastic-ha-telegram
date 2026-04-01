# Meshtastic — Estado del proyecto

## Nodos propios

| Nodo | Dispositivo |
|------|------------|
| **Carlosmdq fijo solar** | Seeed XIAO S3 |
| **Carlosmdq movil** | Heltec V3 |

- **206 nodos** en la red regional AR
- **110 device_trackers** en HA, 109 con GPS

## Integración con Home Assistant

### Conexión TCP directa

- HA conecta al nodo vía integración Meshtastic nativa (puerto TCP 4403)
- **Limitación**: la conexión TCP es exclusiva — si HA está conectado, la app Meshtastic móvil NO puede conectar simultáneamente
- **Workaround**: para usar la app, deshabilitar la integración Meshtastic en HA (disabled_by=user en config_entries + restart)
- **TCP proxy de HA**: escucha pero NO funciona con la app porque no replica el handshake inicial del nodo

### MQTT local (Mosquitto)

- **Broker**: Mosquitto en Docker (puerto 1883), `allow_anonymous`
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

Para cambiar la config MQTT del nodo, usar el meshtastic CLI:

```bash
meshtastic --host <IP_NODO> --set mqtt.address <IP_MOSQUITTO>
meshtastic --host <IP_NODO> --set mqtt.json true
meshtastic --host <IP_NODO> --set mqtt.encryption_enabled false
```

## Archivos

- **Guía completa PDF**: `meshtastic-ha-telegram-guia.pdf` (en esta carpeta)
- **Generador PDF**: `docs/generar-guia.py`

## Pendientes

| Tarea | Estado |
|-------|--------|
| Resolver mapa Meshtastic en dashboard (panel custom redirige a "red-mesh", no carga vista "mapa") | Pendiente |
