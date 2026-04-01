#!/usr/bin/env python3
"""Genera PDF: Guía Meshtastic + Home Assistant + Telegram"""

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Meshtastic + Home Assistant + Telegram - Guía de integración', align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')

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
        x = self.get_x()
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

# === PORTADA ===
pdf.ln(30)
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(0, 100, 180)
pdf.cell(0, 15, 'Meshtastic + Home Assistant', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 15, '+ Telegram', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, 'Guía completa de integración', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.cell(0, 8, 'Enviar y recibir mensajes Meshtastic desde Telegram', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, '31 de marzo de 2026', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, '@carlosmdq', align='C', new_x="LMARGIN", new_y="NEXT")

# === PÁGINA 2: Introducción ===
pdf.add_page()
pdf.titulo('Introducción')
pdf.parrafo(
    'Esta guía explica cómo integrar un nodo Meshtastic con Home Assistant y un bot de Telegram '
    'para poder enviar y recibir mensajes de la red mesh directamente desde el celular, '
    'sin necesidad de tener la app Meshtastic abierta ni estar cerca del nodo.'
)

pdf.subtitulo('El problema')
pdf.parrafo(
    'Meshtastic permite una sola conexión TCP/BLE al nodo a la vez. Si Home Assistant está '
    'conectado al nodo via TCP (para monitorear la red, recibir telemetría, etc.), la app '
    'Meshtastic del celular no puede conectarse simultáneamente.'
)
pdf.parrafo(
    'Esto significa que no podés ver los mensajes directos (DMs) ni enviar mensajes desde la '
    'app mientras HA está conectado.'
)

pdf.subtitulo('La solución')
pdf.parrafo(
    'Se combinan tres componentes para resolver el problema:'
)
pdf.bullet('MQTT local (Mosquitto): el nodo publica mensajes a un broker MQTT accesible por HA y otros servicios.')
pdf.bullet('Automatización en HA: detecta mensajes directos recibidos y los reenvía por Telegram.')
pdf.bullet('Bot de Telegram: comando /mesh que envía mensajes por Meshtastic a través de un webhook de HA.')
pdf.ln(4)

pdf.subtitulo('Arquitectura')
pdf.codigo(
    '  Meshtastic Node\n'
    '       |\n'
    '       |--- TCP (4403) ---> Home Assistant\n'
    '       |                        |\n'
    '       |--- MQTT (1883) --> Mosquitto --> HA (lectura)\n'
    '       |                                     |\n'
    '       |                              Automatización\n'
    '       |                              DM recibido\n'
    '       |                                     |\n'
    '       |                              Telegram Bot\n'
    '       |                              (notificación)\n'
    '       |\n'
    '  Telegram Bot (/mesh)\n'
    '       |\n'
    '       |--- HTTP webhook --> HA --> meshtastic.send_text\n'
    '       |                            (via TCP al nodo)\n'
)

# === REQUISITOS ===
pdf.add_page()
pdf.titulo('Requisitos')

pdf.subtitulo2('Hardware')
pdf.bullet('Nodo Meshtastic con WiFi (ej: Heltec V3, Seeed XIAO S3, T-Beam)')
pdf.bullet('Servidor con Docker (para HA y Mosquitto)')
pdf.ln(2)

pdf.subtitulo2('Software')
pdf.bullet('Home Assistant (Docker o HA OS)')
pdf.bullet('Integración Meshtastic para HA (HACS): github.com/meshtastic/home-assistant')
pdf.bullet('Eclipse Mosquitto (Docker)')
pdf.bullet('Bot de Telegram con token de BotFather')
pdf.bullet('Python 3.10+ (para el bot)')
pdf.ln(2)

pdf.subtitulo2('Conocimientos previos')
pdf.bullet('Meshtastic configurado y funcionando')
pdf.bullet('Home Assistant con la integración Meshtastic operativa')
pdf.bullet('Bot de Telegram básico funcionando')
pdf.ln(4)

# === PASO 1: MOSQUITTO ===
pdf.titulo('Paso 1: Instalar Mosquitto')
pdf.parrafo('Mosquitto es un broker MQTT liviano. Lo levantamos con Docker:')

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

pdf.parrafo('Levantar con:')
pdf.codigo('docker compose up -d')

pdf.nota(
    'Nota: allow_anonymous true es aceptable en una red local. Para exponer a internet, '
    'configurar usuario y password.'
)

# === PASO 2: CONFIGURAR NODO ===
pdf.add_page()
pdf.titulo('Paso 2: Configurar MQTT en el nodo')
pdf.parrafo(
    'Hay dos formas de configurar el MQTT del nodo: desde la app Meshtastic o con Python.'
)

pdf.subtitulo2('Opción A: Desde la app Meshtastic')
pdf.parrafo('Ir a Settings -> Module Configuration -> MQTT y configurar:')
pdf.bullet('Enabled: ON')
pdf.bullet('Server: IP de tu servidor (donde corre Mosquitto)')
pdf.bullet('Puerto: 1883')
pdf.bullet('Username/Password: vacío (si es allow_anonymous)')
pdf.bullet('Encryption enabled: OFF (para que HA lea los mensajes en texto plano)')
pdf.bullet('JSON enabled: ON (formato legible)')
pdf.bullet('Root topic: msh/AR (o el que uses en tu región)')
pdf.bullet('Map reporting: ON (opcional, para posiciones)')
pdf.ln(2)

pdf.subtitulo2('Opción B: Con Python (remoto, sin app)')
pdf.parrafo(
    'Si no podés conectarte con la app (HA ocupa la conexión), podés configurar '
    'el nodo por Python. Primero desactivá la integración Meshtastic en HA, luego:'
)
pdf.codigo(
    'pip install meshtastic\n\n'
    'python3 -c "\n'
    'import meshtastic, meshtastic.tcp_interface, time\n'
    'iface = meshtastic.tcp_interface.TCPInterface(\'IP_DEL_NODO\')\n'
    'time.sleep(3)\n'
    'node = iface.getNode(\'^local\')\n'
    'node.moduleConfig.mqtt.enabled = True\n'
    'node.moduleConfig.mqtt.address = \'IP_DE_MOSQUITTO\'\n'
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

pdf.subtitulo2('Verificar que llegan mensajes')
pdf.codigo(
    'docker exec mosquitto mosquitto_sub -t \'msh/#\' -v'
)
pdf.parrafo('Deberías ver paquetes JSON del nodo cada pocos segundos.')

# === PASO 3: INTEGRACIÓN HA ===
pdf.add_page()
pdf.titulo('Paso 3: Integración MQTT en HA')
pdf.parrafo(
    'Configurar la integración MQTT en Home Assistant (si no la tenés):'
)
pdf.bullet('Ir a Ajustes -> Integraciones -> Agregar -> MQTT')
pdf.bullet('Broker: IP de Mosquitto (puede ser localhost si corre en el mismo server)')
pdf.bullet('Puerto: 1883')
pdf.bullet('Dejar usuario/password vacío si es anonymous')
pdf.ln(2)
pdf.parrafo(
    'La integración Meshtastic de HA sigue conectada por TCP al nodo. '
    'MQTT es un canal adicional de lectura, no reemplaza la conexión TCP.'
)

# === PASO 4: AUTOMATIZACIÓN DM -> TELEGRAM ===
pdf.add_page()
pdf.titulo('Paso 4: Automatización DM -> Telegram')
pdf.parrafo(
    'Esta automatización detecta mensajes directos (PKI) recibidos por el nodo '
    'y los reenvía a Telegram.'
)

pdf.subtitulo2('Requisito previo: REST command para Telegram')
pdf.parrafo('En configuration.yaml de HA, agregar (si no lo tenés):')
pdf.codigo(
    'rest_command:\n'
    '  telegram_notify:\n'
    '    url: "https://api.telegram.org/bot<TU_BOT_TOKEN>/sendMessage"\n'
    '    method: POST\n'
    '    content_type: "application/json"\n'
    '    payload: >-\n'
    '      {"chat_id": <TU_CHAT_ID>,\n'
    '       "text": "{{ title }}\\n{{ message }}",\n'
    '       "parse_mode": "HTML"}'
)

pdf.subtitulo2('Automatización en automations.yaml')
pdf.codigo(
    '- id: \'mesh_dm_a_telegram\'\n'
    '  alias: "Mesh: DM recibido -> Telegram"\n'
    '  description: "Reenvia DMs de Meshtastic a Telegram"\n'
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
    '          De: {{ trigger.event.data.from_name }}\n'
    '          Mensaje: {{ trigger.event.data.message }}'
)

pdf.nota(
    'pki == true filtra solo mensajes directos (encriptados punto a punto). '
    'Si querés recibir TODOS los mensajes del canal, cambiá la condición a pki == false.'
)

# === PASO 5: WEBHOOK PARA ENVIAR ===
pdf.add_page()
pdf.titulo('Paso 5: Webhook para enviar mensajes')
pdf.parrafo(
    'Creamos una automatización con trigger webhook que recibe un POST con el mensaje '
    'y lo envía por Meshtastic. Los webhooks de HA no requieren autenticación.'
)

pdf.subtitulo2('Automatización en automations.yaml')
pdf.codigo(
    '- id: \'mesh_enviar_desde_telegram\'\n'
    '  alias: "Mesh: Enviar mensaje (webhook)"\n'
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

pdf.subtitulo2('Probar el webhook')
pdf.codigo(
    '# Canal publico:\n'
    'curl -X POST http://localhost:8123/api/webhook/mesh_send_from_telegram \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"message": "Hola desde HA"}\'\n\n'
    '# DM a un nodo:\n'
    'curl -X POST http://localhost:8123/api/webhook/mesh_send_from_telegram \\\n'
    '  -H "Content-Type: application/json" \\\n'
    '  -d \'{"message": "Hola", "to": "!abcd1234"}\''
)

pdf.nota('local_only: true significa que solo acepta peticiones desde la red local.')

# === PASO 6: BOT TELEGRAM ===
pdf.add_page()
pdf.titulo('Paso 6: Comando /mesh en el bot')
pdf.parrafo(
    'Si tenés un bot de Telegram en Python, agregar un comando /mesh que llame al webhook:'
)

pdf.subtitulo2('Función para enviar')
pdf.codigo(
    'import requests\n\n'
    'def mesh_send_message(text, to=None):\n'
    '    """Envia mensaje por Meshtastic via webhook de HA."""\n'
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

pdf.subtitulo2('Handler del comando')
pdf.codigo(
    '# En el handler de mensajes del bot:\n'
    'if cmd == "/mesh":\n'
    '    parts = text.split(maxsplit=1)\n'
    '    if len(parts) < 2:\n'
    '        # Mostrar ayuda\n'
    '        send("Uso:\\n/mesh Hola  (canal publico)\\n"\n'
    '             "/mesh @node_id Hola  (DM)")\n'
    '        return\n'
    '    msg = parts[1]\n'
    '    to_node = None\n'
    '    if msg.startswith("@"):\n'
    '        dm_parts = msg.split(maxsplit=1)\n'
    '        to_node = dm_parts[0][1:]  # quitar @\n'
    '        msg = dm_parts[1] if len(dm_parts) > 1 else ""\n'
    '    result = mesh_send_message(msg, to=to_node)\n'
    '    if result["ok"]:\n'
    '        send("Enviado por Meshtastic")\n'
    '    else:\n'
    '        send(f"Error: {result}")'
)

# === NOTAS FINALES ===
pdf.add_page()
pdf.titulo('Notas importantes')

pdf.subtitulo2('Conexión exclusiva TCP')
pdf.parrafo(
    'Meshtastic solo acepta UNA conexión TCP a la vez. Si HA está conectado, '
    'la app del celular no puede conectarse simultáneamente al mismo nodo. '
    'Opciones para acceder al nodo:'
)
pdf.bullet('Usar Bluetooth (BLE) desde la app si estás cerca del nodo.')
pdf.bullet('Desactivar temporalmente la integración Meshtastic en HA.')
pdf.bullet('Usar el panel web de Meshtastic integrado en HA (solo lectura).')
pdf.ln(2)

pdf.subtitulo2('TCP Proxy de HA')
pdf.parrafo(
    'La integración Meshtastic tiene un TCP proxy que permite conexiones de apps '
    'a través de HA. Sin embargo, en la práctica la app da "too many retries" '
    'porque el proxy no replica el handshake inicial que el nodo envía al conectar. '
    'No es una solución confiable actualmente.'
)

pdf.subtitulo2('MQTT: encryption off')
pdf.parrafo(
    'Para que HA pueda leer los mensajes en JSON, la encriptación MQTT debe estar '
    'desactivada en el nodo. Esto significa que los mensajes viajan en texto plano '
    'por la red local. Es aceptable en una LAN hogareña, pero si exponés el broker '
    'a internet, configurá TLS y autenticación.'
)

pdf.subtitulo2('Eventos en HA')
pdf.parrafo('La integración Meshtastic dispara estos eventos que podés usar en automatizaciones:')
pdf.bullet('meshtastic_message_log - mensajes con from_name, message, pki (true=DM)')
pdf.bullet('meshtastic_event - eventos de dispositivos (message.received, message.sent)')
pdf.bullet('meshtastic_api_text_message - detalle completo del mensaje con from/to/channel')
pdf.bullet('meshtastic_api_position - posiciones GPS de nodos')
pdf.bullet('meshtastic_api_telemetry - batería, señal, uptime de nodos')
pdf.ln(4)

pdf.subtitulo2('Device triggers disponibles')
pdf.parrafo('En el dispositivo gateway podés crear automatizaciones con triggers:')
pdf.bullet('message.received - cualquier mensaje recibido')
pdf.bullet('direct_message.received - DM recibido')
pdf.bullet('channel_message.received - mensaje en canal')
pdf.bullet('message.sent / direct_message.sent / channel_message.sent')


output = '/home/carlosmdq/proyectos/meshtastic/docs/meshtastic-ha-telegram-guia.pdf'
pdf.output(output)
print(f'PDF generado: {output}')
