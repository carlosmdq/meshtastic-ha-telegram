"""
Comando /mesh para bot de Telegram — envía mensajes por Meshtastic via Home Assistant.

Uso:
    /mesh Hola a todos          → canal público
    /mesh @node_id Hola         → DM a nodo específico

Requisitos:
    - Home Assistant con automatización 'mesh_enviar_desde_telegram' (webhook)
    - Bot de Telegram con python-telegram-bot o aiohttp
    - requests

Integración:
    Este código se integra en el handler de comandos del bot.
    La URL del webhook apunta a HA en la misma red local.
"""

import requests

# Ajustar a la IP:puerto de tu Home Assistant
HA_WEBHOOK_URL = "http://127.0.0.1:8123/api/webhook/mesh_send_from_telegram"


def mesh_send_message(text: str, to: str = None) -> dict:
    """Envía mensaje por Meshtastic via webhook de HA (sin auth requerido)."""
    try:
        payload = {"message": text}
        if to:
            payload["to"] = to
        resp = requests.post(HA_WEBHOOK_URL, json=payload, timeout=15)
        return {"ok": resp.status_code == 200, "status": resp.status_code}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def handle_mesh_command(text: str) -> dict:
    """
    Parsea el comando /mesh y envía el mensaje.

    Args:
        text: texto después de '/mesh ', ej: "Hola" o "@12345 Hola"

    Returns:
        dict con resultado: {"ok": bool, "dest": str, "message": str}
    """
    if not text.strip():
        return {
            "ok": False,
            "error": "Uso: /mesh texto  |  /mesh @node_id texto"
        }

    msg_text = text.strip()
    to_node = None

    # Si empieza con @ es DM a un nodo específico
    if msg_text.startswith("@"):
        parts = msg_text.split(maxsplit=1)
        to_node = parts[0][1:]  # quitar @
        msg_text = parts[1] if len(parts) > 1 else ""

    if not msg_text:
        return {"ok": False, "error": "Falta el mensaje a enviar"}

    result = mesh_send_message(msg_text, to=to_node)
    dest = f"DM a {to_node}" if to_node else "Canal público"

    return {
        "ok": result.get("ok", False),
        "dest": dest,
        "message": msg_text,
        "error": result.get("error")
    }
