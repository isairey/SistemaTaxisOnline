# 🚖 Sistema de Taxis Online

Aplicación web fullstack para la gestión de un sistema de taxis en línea, permitiendo administrar usuarios, servicios y operaciones mediante una plataforma digital moderna.

---

## 📌 Descripción

El **Sistema de Taxis Online** es una solución desarrollada para facilitar la administración y operación de servicios de transporte, integrando una interfaz web, autenticación de usuarios y un backend eficiente.

El sistema permite centralizar la información y mejorar la organización de los procesos operativos.

---

## 🚀 Características

- 🌐 Interfaz web interactiva
- 🔐 Sistema de autenticación de usuarios
- 🚖 Gestión de servicios de taxis
- 📋 Administración de registros
- ⚡ API REST para comunicación cliente-servidor
- 💾 Manejo de base de datos

---

## 🛠️ Tecnologías utilizadas

### Backend
- **Python**
- **FastAPI**

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**

### Otros
- **Flet**
- **Uvicorn**
- **PostgreSQL**

---

## 📂 Estructura del proyecto

```
sistema-taxis/
│
├── 📁 Backend/
├── 📁 Frontend/
├── 📁 landing/
├── 📁 backups/
├── 📁 env/
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/tuusuario/sistema-taxis.git
cd sistema-taxis
```
### 2. Crear entorno virtual
```
Windows
python -m venv env
env\Scripts\activate
Linux / Mac
python3 -m venv env
source env/bin/activate
```
### 3. Instalar dependencias
```
pip install -r requirements.txt
```
---
## ▶️ Ejecución
```
Backend
uvicorn Backend.main:app --reload
Frontend
python Frontend/app.py
Landing Page
```
Abrir en navegador:
```
landing/index.html
```
---
## 🗄️ Base de datos

Motor: PostgreSQL
Backup disponible en:
```
/backups/mi_base.sql
```
---

## 💡 Funcionamiento

El sistema opera mediante la conexión entre frontend y backend a través de una API REST, permitiendo gestionar la información en tiempo real.

---

## 📈 Mejoras futuras

- 📱 Aplicación móvil
- 📊 Panel de administración avanzado
- 🔔 Notificaciones en tiempo real
- ☁️ Despliegue en la nube
---
## 👨‍💻 Autor

Desarrollado por Isai Reyes Peña

---
## 📄 Licencia

License MIT.
