# 🧠 PsicoAgenda — Sistema de citas psicológicas

Aplicación web completa para gestión de citas psicológicas con:
- Login y registro de usuarios
- Panel admin (psicólogo) y panel paciente
- Gestión de citas (agendar, confirmar, cancelar)
- Base de datos SQLite (local) o PostgreSQL (nube)

---

## 🚀 Opción 1: Railway (GRATIS, recomendado)

1. Ir a https://railway.app y crear cuenta gratuita
2. Clic en **"New Project"** → **"Deploy from GitHub repo"**
3. Subir tu código a GitHub primero, luego conectarlo
4. Railway detecta automáticamente el Procfile
5. Agregar una base de datos PostgreSQL:
   - En el proyecto, clic en **"+ New"** → **"Database"** → **"PostgreSQL"**
   - Railway automáticamente agrega `DATABASE_URL` como variable de entorno
6. En Variables de entorno agregar:
   - `SECRET_KEY` = (cualquier texto largo y aleatorio, ej: `mi-clave-super-secreta-2024`)
7. Deploy automático ✅

---

## 🚀 Opción 2: Render (GRATIS)

1. Ir a https://render.com y crear cuenta
2. **New** → **Web Service** → conectar tu repositorio GitHub
3. Configurar:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Crear base de datos gratuita:
   - **New** → **PostgreSQL** (plan Free)
   - Copiar la **Internal Database URL**
5. En Variables de entorno del web service:
   - `DATABASE_URL` = (la URL de tu base de datos)
   - `SECRET_KEY` = (texto aleatorio largo)
6. Deploy ✅

---

## 🚀 Opción 3: Local (para pruebas)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

Abrir: http://localhost:5000

---

## 🔑 Cuentas de demo (se crean automáticamente)

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Admin (psicólogo) | admin@psico.com | admin123 |
| Paciente | ana@demo.com | paciente123 |

---

## 📁 Estructura del proyecto

```
psicoagenda/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias Python
├── Procfile           # Configuración servidor
├── README.md
└── templates/
    ├── base.html
    ├── login.html
    ├── registro.html
    ├── dashboard_admin.html
    ├── dashboard_paciente.html
    ├── citas.html
    └── pacientes.html
```

---

## ⚙️ Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta Flask | `mi-clave-2024-abc` |
| `DATABASE_URL` | URL de PostgreSQL | `postgresql://user:pass@host/db` |
| `PORT` | Puerto (Railway/Render lo ponen automático) | `5000` |

---

## 🛠️ Cómo crear un admin nuevo

Después de desplegar, para crear nuevos psicólogos/admins:
1. Registrarse normalmente en la app
2. Conectarse a la base de datos y cambiar `rol` de `'paciente'` a `'admin'`

En Railway/Render puedes usar la consola de PostgreSQL o conectarte con DBeaver.
