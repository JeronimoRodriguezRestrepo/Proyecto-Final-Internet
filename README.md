# Proyecto Final — Internet: Arquitectura y Protocolos


## Integrantes
- Jerónimo Rodríguez Restrepo
- Simón Tovar Tabares

## Descripción
Sistema web desplegado en AWS compuesto por un balanceador de carga NGINX con proxy inverso y SSL, dos servidores de aplicación Flask (uno en inglés y otro en español), una base de datos MySQL y un script de estadísticas con envío de correo automático.

**URL pública:** https://proyectofinal.ddns.net

## Arquitectura

## Arquitectura

| Máquina | Rol | Puerto |
|---------|-----|--------|
| SW1 | Balanceador NGINX + SSL | 80, 443 |
| SW2 | Web Server 1 (inglés) | 5000 |
| SW3 | Web Server 2 (español) | 5000 |
| SW4 | Base de datos MySQL | 3306 |

## Estructura del repositorio

```
/
├── app_en/              # Web Server 1 — formulario en inglés
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   └── Dockerfile
├── app_es/              # Web Server 2 — formulario en español
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   └── Dockerfile
├── balanceador/         # NGINX round robin + SSL
│   ├── nginx/
│   │   └── nginx.conf
│   └── docker-compose.yml
├── database/            # MySQL en Docker
│   └── docker-compose.yml
├── stats/               # Script de estadísticas
│   └── stats.py
├── Rodriguez_Tovar.pdf  # Documentación del proyecto
└── README.md
```

## Tecnologías utilizadas
- **AWS EC2** — 4 instancias Ubuntu 24.04
- **Docker** — contenerización de todos los servicios
- **NGINX** — balanceador de carga round robin + proxy inverso
- **Let's Encrypt** — certificado SSL gratuito
- **Flask (Python)** — aplicaciones web
- **MySQL 8.0** — base de datos
- **No-IP** — dominio gratuito con registro DNS tipo A

## Despliegue
Cada componente corre en un contenedor Docker independiente. Ver `Rodriguez_Tovar.pdf` para instrucciones detalladas de configuración y despliegue.

## Script de estadísticas
Envía un correo a `ialondonoo@eafit.edu.co` con gráficas de registros por comuna, carrera y servidor.

```bash
cd ~/stats
python3 stats.py
```

> Las credenciales SMTP se configuran en un archivo `.env` (excluido del repositorio).
