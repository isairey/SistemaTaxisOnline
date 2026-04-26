# San Agatón - Gestión de Base de Datos y Aplicación Web

Aplicación web fullstack para la gestión de la línea de taxis **San Agatón**, integrando landing page, login con Flet, backend con FastAPI y base de datos PostgreSQL.

---

## Estructura del proyecto

```plaintext
san-agaton/
│
├─ Backend/          # Backend FastAPI
├─ Frontend/         # Archivos JS, CSS y recursos
├─ landing/          # Landing page HTML, CSS y JS
├─ backups/          # Backups de la base de datos
│   └─ mi_base.sql
├─ env/              # Entorno virtual (ignorado en Git)
├─ requirements.txt  # Dependencias del proyecto
└─ README.md         # Este archivo

## Crear y activar el entorno virtual:

Windows:
python -m venv env
env\Scripts\activate

Linux:
python3 -m venv env
source env/bin/activate

##Instalar Dependencias

pip install -r requirements.txt


## Servidor Fastapi y de flet

frontend flet:

py Frontend/app.py

si no se hace así, al utilizar la landing page, no le redireccione a Login.py de flet.

correr en el entorno virtual en el servidor local para correr el backend:

uvicorn Backend.main:app --reload

## Licencia

Este proyecto está bajo **MIT License** (en inglés).  
En resumen, puedes usar, modificar y redistribuir el proyecto, incluso con fines comerciales, siempre que mantengas el aviso de copyright original.

>Nota: Este proyecto es una entrega académica para la universidad y se presenta solo con fines educativos.
