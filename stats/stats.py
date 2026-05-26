import pymysql
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Configuración ──────────────────────────────────────────
load_dotenv('/home/ubuntu/stats/.env')

DB_CONFIG = {
    'host': '172.31.28.189',
    'user': 'eafit',
    'password': 'eafit2025',
    'database': 'registros',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
DEST_EMAIL = 'ialondonoo@eafit.edu.co'

# ── Consultar BD ───────────────────────────────────────────
conn = pymysql.connect(**DB_CONFIG)
with conn.cursor() as cur:
    cur.execute("SELECT comuna, carrera, servidor FROM registros")
    rows = cur.fetchall()
conn.close()

print(f"Total registros: {len(rows)}")

# ── Procesar datos ─────────────────────────────────────────
comunas = {}
carreras = {}
servidores = {}

for r in rows:
    c = r['comuna']
    k = r['carrera']
    s = r['servidor']
    comunas[c] = comunas.get(c, 0) + 1
    carreras[k] = carreras.get(k, 0) + 1
    servidores[s] = servidores.get(s, 0) + 1

# ── Grafica 1: por comuna ──────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar([f"Comuna {k}" for k in sorted(comunas)], [comunas[k] for k in sorted(comunas)], color='#003087')
ax1.set_title('Registros por Comuna')
ax1.set_ylabel('Cantidad')
plt.tight_layout()
fig1.savefig('/tmp/grafica_comunas.png')
plt.close()

# ── Grafica 2: por carrera ─────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.pie(carreras.values(), labels=carreras.keys(), autopct='%1.1f%%',
        colors=['#003087','#0057b7','#4a90d9','#a8d1f0'])
ax2.set_title('Registros por Carrera')
plt.tight_layout()
fig2.savefig('/tmp/grafica_carreras.png')
plt.close()

# ── Grafica 3: por servidor ────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(5, 4))
ax3.bar(servidores.keys(), servidores.values(), color=['#003087','#0057b7'])
ax3.set_title('Registros por Servidor')
ax3.set_ylabel('Cantidad')
plt.tight_layout()
fig3.savefig('/tmp/grafica_servidores.png')
plt.close()

# ── Armar correo ───────────────────────────────────────────
msg = MIMEMultipart('related')
msg['Subject'] = 'Estadísticas EAFIT — Proyecto Final'
msg['From'] = SMTP_USER
msg['To'] = DEST_EMAIL

html = f"""
<h2>Estadísticas del Sistema de Registro EAFIT</h2>
<p><strong>Total de registros:</strong> {len(rows)}</p>

<h3>Por Comuna</h3>
<img src="cid:comunas">

<h3>Por Carrera</h3>
<img src="cid:carreras">

<h3>Por Servidor</h3>
<img src="cid:servidores">
"""

msg.attach(MIMEText(html, 'html'))

for cid, path in [('comunas', '/tmp/grafica_comunas.png'),
                   ('carreras', '/tmp/grafica_carreras.png'),
                   ('servidores', '/tmp/grafica_servidores.png')]:
    with open(path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', f'<{cid}>')
        msg.attach(img)

# ── Enviar ─────────────────────────────────────────────────
with smtplib.SMTP('smtp.gmail.com', 587) as s:
    s.starttls()
    s.login(SMTP_USER, SMTP_PASS)
    s.sendmail(SMTP_USER, DEST_EMAIL, msg.as_string())

print(f"✅ Correo enviado a {DEST_EMAIL}")
