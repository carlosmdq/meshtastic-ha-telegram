"""
/mesh command for Telegram bot — sends messages via Meshtastic through Home Assistant.

Usage:
    /mesh Hello everyone        → public channel
    /mesh @node_id Hello        → DM to specific node

Requirements:
    - Home Assistant with 'mesh_enviar_desde_telegram' automation (webhook)
    - Telegram bot with python-telegram-bot or aiohttp
    - requests

Integration:
    This code integrates into your bot's command handler.
    The webhook URL points to HA on the same local network.
"""

import requests

# Adjust to your Home Assistant IP:port
HA_WEBHOOK_URL = "http://127.0.0.1:8123/api/webhook/mesh_send_from_telegram"


def mesh_send_message(text: str, to: str = None) -> dict:
    """Send a message via Meshtastic through HA webhook (no auth required)."""
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
    Parse the /mesh command and send the message.

    Args:
        text: text after '/mesh ', e.g.: "Hello" or "@12345 Hello"

    Returns:
        dict with result: {"ok": bool, "dest": str, "message": str}
    """
    if not text.strip():
        return {
            "ok": False,
            "error": "Usage: /mesh text  |  /mesh @node_id text"
        }

    msg_text = text.strip()
    to_node = None

    # If starts with @ it's a DM to a specific node
    if msg_text.startswith("@"):
        parts = msg_text.split(maxsplit=1)
        to_node = parts[0][1:]  # remove @
        msg_text = parts[1] if len(parts) > 1 else ""

    if not msg_text:
        return {"ok": False, "error": "Missing message text"}

    result = mesh_send_message(msg_text, to=to_node)
    dest = f"DM to {to_node}" if to_node else "Public channel"

    return {
        "ok": result.get("ok", False),
        "dest": dest,
        "message": msg_text,
        "error": result.get("error")
    }
