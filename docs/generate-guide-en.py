#!/usr/bin/env python3
"""Generate PDF: Meshtastic + Home Assistant + Telegram Integration Guide (English)"""

from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Meshtastic + Home Assistant + Telegram - Integration Guide', align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def titulo(self, texto):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(30, 30, 30)
        self.cell(0, 12, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def subtitulo(self, texto):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(50, 50, 50)
        self.ln(4)
        self.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 120, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)

    def subtitulo2(self, texto):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(70, 70, 70)
        self.ln(2)
        self.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def parrafo(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, texto)
        self.ln(2)

    def codigo(self, texto):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(30, 30, 30)
        w = self.w - self.l_margin - self.r_margin
        self.multi_cell(w, 5, texto, fill=True)
        self.ln(3)

    def bullet(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        x0 = self.l_margin
        self.set_x(x0)
        self.cell(8, 5.5, '- ')
        self.multi_cell(self.w - self.r_margin - x0 - 8, 5.5, texto)

    def nota(self, texto):
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.set_fill_color(255, 255, 230)
        self.multi_cell(0, 5, texto, fill=True)
        self.ln(2)


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# === COVER ===
pdf.ln(30)
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(0, 100, 180)
pdf.cell(0, 15, 'Meshtastic + Home Assistant', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 15, '+ Telegram', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, 'Complete Integration Guide', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.cell(0, 8, 'Send and receive Meshtastic messages from Telegram', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, 'March 31, 2026', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, '@carlosmdq', align='C', new_x="LMARGIN", new_y="NEXT")

# === PAGE 2: Introduction ===
pdf.add_page()
pdf.titulo('Introduction')
pdf.parrafo(
    'This guide explains how to integrate a Meshtastic node with Home Assistant and a Telegram bot '
    'to send and receive mesh network messages directly from your phone, '
    'without needing the Meshtastic app open or being near the node.'
)

pdf.subtitulo('The Problem')
pdf.parrafo(
    'Meshtastic only allows one TCP/BLE connection to the node at a time. If Home Assistant is '
    'connected to the node via TCP (to monitor the network, receive telemetry, etc.), the '
    'Meshtastic mobile app cannot connect simultaneously.'
)
pdf.parrafo(
    'This means you cannot see direct messages (DMs) or send messages from the app '
    'while HA is connected.'
)

pdf.subtitulo('The Solution')
pdf.parrafo(
    'Three components are combined to solve the problem:'
)
pdf.bullet('Local MQTT (Mosquitto): the node publishes messages to an MQTT broker accessible by HA and other services.')
pdf.bullet('HA Automation: detects received direct messages and forwards them to Telegram.')
pdf.bullet('Telegram Bot: /mesh command that sends messages via Meshtastic through an HA webhook.')
pdf.ln(4)

pdf.subtitulo('Architecture')
pdf.codigo(
    '  Meshtastic Node\n'
    '       |\n'
    '       |--- TCP (4403) ---> Home Assistant\n'
    '       |                        |\n'
    '       |--- MQTT (1883) --> Mosquitto --> HA (read)\n'
    '       |                                     |\n'
    '       |                              Automation\n'
    '       |                              DM received\n'
    '       |                                     |\n'
    '       |                              Telegram Bot\n'
    '       |                              (notification)\n'
    '       |\n'
    '  Telegram Bot (/mesh)\n'
    '       |\n'
    '       |--- HTTP webhook --> HA --> meshtastic.send_text\n'
    '       |                            (via TCP to node)\n'
)

# === REQUIREMENTS ===
pdf.add_page()
pdf.titulo('Requirements')

pdf.subtitulo2('Hardware')
pdf.bullet('Meshtastic node with WiFi (e.g.: Heltec V3, Seeed XIAO S3, T-Beam)')
pdf.bullet('Server with Docker (for HA and Mosquitto)')
pdf.ln(2)

pdf.subtitulo2('Software')
pdf.bullet('Home Assistant (Docker or HA OS)')
pdf.bullet('Meshtastic Integration for HA (HACS): github.com/meshtastic/home-assistant')
pdf.bullet('Eclipse Mosquitto (Docker)')
pdf.bullet('Telegram Bot with BotFather token')
pdf.bullet('Python 3.10+ (for the bot)')
pdf.ln(2)

pdf.subtitulo2('Prerequisites')
pdf.bullet('Meshtastic configured and working')
pdf.bullet('Home Assistant with Meshtastic integration operational')
pdf.bullet('Basic Telegram bot running')
pdf.ln(4)

# === STEP 1: MOSQUITTO ===
pdf.titulo('Step 1: Install Mosquitto')
pdf.parrafo('Mosquitto is a lightweight MQTT broker. We run it with Docker:')

pdf.subtitulo2('docker-compose.yml')
pdf.codigo(
    'services:\n'
    '  mosquitto:\n'
    '    container_name: mosquitto\n'
    '    image: eclipse-mosquitto:2\n'
    '    restart: unless-stopped\n'
    '    ports:\n'
    '      - "1883:1883"\n'
    '    volumes:\n'
    '      - ./config:/mosquitto/config\n'
    '      - ./data:/mosquitto/data\n'
    '      - ./log:/mosquitto/log'
)

pdf.subtitulo2('config/mosquitto.conf')
pdf.codigo(
    'listener 1883\n'
    'allow_anonymous true\n'
    'persistence true\n'
    'persistence_location /mosquitto/data/\n'
    'log_dest file /mosquitto/log/mosquitto.log'
)

pdf.parrafo('Start with:')
pdf.codigo('docker compose up -d')

pdf.nota(
    'Note: allow_anonymous true is acceptable on a local network. To expose to the internet, '
    'configure username and password.'
)

# === STEP 2: CONFIGURE NODE ===
pdf.add_page()
pdf.titulo('Step 2: Configure MQTT on the Node')
pdf.parrafo(
    'There are two ways to configure the node\'s MQTT: from the Meshtastic app or with Python.'
)

pdf.subtitulo2('Option A: From the Meshtastic App')
pdf.parrafo('Go to Settings -> Module Configuration -> MQTT and configure:')
pdf.bullet('Enabled: ON')
pdf.bullet('Server: Your server IP (where Mosquitto runs)')
pdf.bullet('Port: 1883')
pdf.bullet('Username/Password: empty (if allow_anonymous)')
pdf.bullet('Encryption enabled: OFF (so HA can read messages in plain text)')
pdf.bullet('JSON enabled: ON (readable format)')
pdf.bullet('Root topic: msh/AR (or your region\'s topic)')
pdf.bullet('Map reporting: ON (optional, for positions)')
pdf.ln(2)

pdf.subtitulo2('Option B: With Python (remote, no app needed)')
pdf.parrafo(
    'If you can\'t connect with the app (HA occupies the connection), you can configure '
    'the node via Python. First disable the Meshtastic integration in HA, then:'
)
pdf.codigo(
    'pip install meshtastic\n\n'
    'python3 -c "\n'
    'import meshtastic, meshtastic.tcp_interface, time\n'
    'iface = meshtastic.tcp_interface.TCPInterface(\'NODE_IP\')\n'
    'time.sleep(3)\n'
    'node = iface.getNode(\'^local\')\n'
    'node.moduleConfig.mqtt.enabled = True\n'
    'node.moduleConfig.mqtt.address = \'MOSQUITTO_IP\'\n'
    'node.moduleConfig.mqtt.username = \'\'\n'
    'node.moduleConfig.mqtt.password = \'\'\n'
    'node.moduleConfig.mqtt.encryption_enabled = False\n'
    'node.moduleConfig.mqtt.json_enabled = True\n'
    'node.moduleConfig.mqtt.tls_enabled = False\n'
    'node.moduleConfig.mqtt.root = \'msh/AR\'\n'
    'node.moduleConfig.mqtt.map_reporting_enabled = True\n'
    'node.writeConfig(\'mqtt\')\n'
    'time.sleep(3)\n'
    'iface.close()\n'
    '"'
)

pdf.subtitulo2('Verify messages are arriving')
pdf.codigo(
    'docker exec mosquitto mosquitto_sub -t \'msh/#\' -v'
)
pdf.parrafo('You should see JSON packets from the node every few seconds.')

# === STEP 3: HA INTEGRATION ===
pdf.add_page()
pdf.titulo('Step 3: MQTT Integration in HA')
pdf.parrafo(
    'Configure the MQTT integration in Home Assistant (if you don\'t have it):'
)
pdf.bullet('Go to Settings -> Integrations -> Add -> MQTT')
pdf.bullet('Broker: Mosquitto IP (can be localhost if on the same server)')
pdf.bullet('Port: 1883')
pdf.bullet('Leave username/password empty if anonymous')
pdf.ln(2)
pdf.parrafo(
    'The Meshtastic HA integration stays connected via TCP to the node. '
    'MQTT is an additional read channel, it does not replace the TCP connection.'
)

# === STEP 4: DM -> TELEGRAM AUTOMATION ===
pdf.add_page()
pdf.titulo('Step 4: DM -> Telegram Automation')
pdf.parrafo(
    'This automation detects direct messages (PKI) received by the node '
    'and forwards them to Telegram.'
)

pdf.subtitulo2('Prerequisite: REST command for Telegram')
pdf.parrafo('In HA\'s configuration.yaml, add (if you don\'t have it):')
pdf.codigo(
    'rest_command:\n'
    '  telegram_notify:\n'
    '    url: "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage"\n'
    '    method: POST\n'
    '    content_type: "application/json"\n'
    '    payload: >-\n'
    '      {"chat_id": <YOUR_CHAT_ID>,\n'
    '       "text": "{{ title }}\\n{{ message }}",\n'
    '       "parse_mode": "HTML"}'
)

pdf.subtitulo2('Automation in automations.yaml')
pdf.codigo(
    '- id: \'mesh_dm_a_telegram\'\n'
    '  alias: "Mesh: DM received -> Telegram"\n'
    '  description: "Forward Meshtastic DMs to Telegram"\n'
    '  mode: queued\n'
    '  trigger:\n'
    '    - platform: event\n'
    '      event_type: meshtastic_message_log\n'
    '  condition:\n'
    '    - condition: template\n'
    '      value_template: "{{ trigger.event.data.pki == true }}"\n'
    '  action:\n'
    '    - action: rest_command.telegram_notify\n'
    '      data:\n'
    '        title: "DM Meshtastic"\n'
    '        message: >-\n'
    '          From: {{ trigger.event.data.from_name }}\n'
    '          Message: {{ trigger.event.data.message }}'
)

pdf.nota(
    'pki == true filters only direct messages (end-to-end encrypted). '
    'To receive ALL channel messages, change the condition to pki == false.'
)

# === STEP 5: SEND WEBHOOK ===
pdf.add_page()
pdf.titulo('Step 5: Webhook to Send Messages')
pdf.parrafo(
    'We create an automation with a webhook trigger that receives a POST with the message '
    'and sends it via Meshtastic. HA webhooks do not require authentication.'
)

pdf.subtitulo2('Automation in automations.yaml')
pdf.codigo(
    '- id: \'mesh_enviar_desde_telegram\'\n'
    '  alias: "Mesh: Send message (webhook)"\n'
    '  mode: queued\n'
    '  trigger:\n'
    '    - platform: webhook\n'
    '      webhook_id: mesh_send_from_telegram\n'
    '      allowed_methods:\n'
    '        - POST\n'
    '      local_only: true\n'
    '  action:\n'
    '    - choose:\n'
    '        - conditions:\n'
    '            - condition: template\n'
    '              value_template: >-\n'
    '                {{ trigger.json.to is defined\n'
    '                   and trigger.json.to }}\n'
    '          sequence:\n'
    '            - action: meshtastic.send_text\n'
    '              data:\n'
    '                text: "{{ trigger.json.message }}"\n'
    '                to: "{{ trigger.json.to }}"\n'
    '                ack: true\n'
    '      default:\n'
    '        - action: meshtastic.send_text\n'
    '          data:\n'
    '            text: "{{ trigger.json.message }}"\n'
    '            ack: true'
)

pdf.subtitulo2('Test the webhook')
pdf.codigo(
    '# Public channel:\n'
    'curl -X POST http://localhost:8123/api/webhook/mesh_send_from_telegram \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"message": "Hello from HA"}\'\n\n'
    '# DM to a node:\n'
    'curl -X POST http://localhost:8123/api/webhook/mesh_send_from_telegram \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"message": "Hello", "to": "!abcd1234"}\''
)

pdf.nota('local_only: true means it only accepts requests from the local network.')

# === STEP 6: TELEGRAM BOT ===
pdf.add_page()
pdf.titulo('Step 6: /mesh Command in the Bot')
pdf.parrafo(
    'If you have a Python Telegram bot, add a /mesh command that calls the webhook:'
)

pdf.subtitulo2('Send function')
pdf.codigo(
    'import requests\n\n'
    'def mesh_send_message(text, to=None):\n'
    '    """Send message via Meshtastic through HA webhook."""\n'
    '    url = "http://localhost:8123/api/webhook/mesh_send_from_telegram"\n'
    '    payload = {"message": text}\n'
    '    if to:\n'
    '        payload["to"] = to\n'
    '    try:\n'
    '        resp = requests.post(url, json=payload, timeout=15)\n'
    '        return {"ok": resp.status_code == 200}\n'
    '    except Exception as e:\n'
    '        return {"ok": False, "error": str(e)}'
)

pdf.subtitulo2('Command handler')
pdf.codigo(
    '# In the bot message handler:\n'
    'if cmd == "/mesh":\n'
    '    parts = text.split(maxsplit=1)\n'
    '    if len(parts) < 2:\n'
    '        # Show help\n'
    '        send("Usage:\\n/mesh Hello  (public channel)\\n"\n'
    '             "/mesh @node_id Hello  (DM)")\n'
    '        return\n'
    '    msg = parts[1]\n'
    '    to_node = None\n'
    '    if msg.startswith("@"):\n'
    '        dm_parts = msg.split(maxsplit=1)\n'
    '        to_node = dm_parts[0][1:]  # remove @\n'
    '        msg = dm_parts[1] if len(dm_parts) > 1 else ""\n'
    '    result = mesh_send_message(msg, to=to_node)\n'
    '    if result["ok"]:\n'
    '        send("Sent via Meshtastic")\n'
    '    else:\n'
    '        send(f"Error: {result}")'
)

# === IMPORTANT NOTES ===
pdf.add_page()
pdf.titulo('Important Notes')

pdf.subtitulo2('Exclusive TCP Connection')
pdf.parrafo(
    'Meshtastic only accepts ONE TCP connection at a time. If HA is connected, '
    'the mobile app cannot connect simultaneously to the same node. '
    'Options to access the node:'
)
pdf.bullet('Use Bluetooth (BLE) from the app if you are near the node.')
pdf.bullet('Temporarily disable the Meshtastic integration in HA.')
pdf.bullet('Use the Meshtastic web panel integrated in HA (read only).')
pdf.ln(2)

pdf.subtitulo2('HA TCP Proxy')
pdf.parrafo(
    'The Meshtastic integration has a TCP proxy that allows app connections '
    'through HA. However, in practice the app gives "too many retries" '
    'because the proxy does not replicate the initial handshake the node sends on connect. '
    'Not a reliable solution currently.'
)

pdf.subtitulo2('MQTT: encryption off')
pdf.parrafo(
    'For HA to read messages in JSON, MQTT encryption must be disabled on the node. '
    'This means messages travel in plain text over the local network. '
    'This is acceptable on a home LAN, but if you expose the broker to the internet, '
    'configure TLS and authentication.'
)

pdf.subtitulo2('HA Events')
pdf.parrafo('The Meshtastic integration fires these events you can use in automations:')
pdf.bullet('meshtastic_message_log - messages with from_name, message, pki (true=DM)')
pdf.bullet('meshtastic_event - device events (message.received, message.sent)')
pdf.bullet('meshtastic_api_text_message - full message detail with from/to/channel')
pdf.bullet('meshtastic_api_position - GPS positions from nodes')
pdf.bullet('meshtastic_api_telemetry - battery, signal, uptime from nodes')
pdf.ln(4)

pdf.subtitulo2('Available Device Triggers')
pdf.parrafo('On the gateway device you can create automations with triggers:')
pdf.bullet('message.received - any message received')
pdf.bullet('direct_message.received - DM received')
pdf.bullet('channel_message.received - channel message')
pdf.bullet('message.sent / direct_message.sent / channel_message.sent')


output = '/home/carlosmdq/proyectos/meshtastic/docs/meshtastic-ha-telegram-guide.pdf'
pdf.output(output)
print(f'PDF generated: {output}')
