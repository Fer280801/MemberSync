MemberSync

Descripción

MemberSync es una aplicación web full-stack diseñada para la gestión de miembros y autenticación segura mediante JWT.

El proyecto está estructurado como un monorepo que contiene:
	•	Backend: FastAPI (Python)
	•	Base de datos: PostgreSQL usando asyncpg
	•	Deploy backend: Render
	•	Frontend: React + Vite (Netlify)
	•	CI/CD: GitHub Actions

⸻

Arquitectura del Sistema

Netlify (Frontend React)
        │
        │ HTTPS
        ▼
Render (FastAPI Backend)
        │
        ▼
PostgreSQL (Neon / Local)

El backend utiliza:
	•	FastAPI
	•	SQLAlchemy Async
	•	asyncpg
	•	Pydantic v2
	•	JWT para autenticación

⸻

Estructura Real del Proyecto

MemberSync/
│
├── backend/
│   ├── app/
│   │   ├── main.py                # App principal FastAPI
│   │   ├── config.py              # Configuración y variables de entorno
│   │   ├── models/                # Modelos SQLAlchemy
│   │   ├── routes/                # Endpoints
│   │   ├── utils/
│   │   │   └── authentication.py  # Manejo de JWT
│   │   └── ...
│   └── requirements.txt
│
├── render.yaml                    # Configuración automática para Render
├── main.py                        # Entry point para Render (exporta app)
├── requirements.txt               # Incluye backend/requirements.txt
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
│
└── README.md

Importante:
El archivo main.py en la raíz importa y expone la aplicación ubicada en backend/app/main.py para que Render pueda ejecutar:

uvicorn main:app


⸻

Requisitos
	•	Python 3.11+
	•	PostgreSQL
	•	Node.js 20+ (para frontend)
	•	Git

⸻

Configuración Local del Backend

1. Clonar repositorio

git clone https://github.com/TU_USUARIO/MemberSync.git
cd MemberSync


⸻

2. Crear entorno virtual

Mac / Linux:

python -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate


⸻

3. Instalar dependencias

pip install -r requirements.txt

El archivo raíz requirements.txt incluye:

-r backend/requirements.txt


⸻

4. Variables de entorno

Crear archivo .env en la raíz del proyecto:

DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/dbname
SECRET_KEY=tu_clave_super_secreta

Notas importantes:
	•	Debe usarse postgresql+asyncpg://
	•	El sistema acepta tanto SECRET_KEY como JWT_SECRET
	•	No subir el archivo .env al repositorio

⸻

5. Ejecutar servidor en desarrollo

uvicorn main:app --reload

Acceder a:

http://localhost:8000/docs


⸻

Configuración de Base de Datos

El backend utiliza SQLAlchemy en modo async.

La variable DATABASE_URL debe tener formato:

postgresql+asyncpg://usuario:password@host:puerto/database

En producción (Render + Neon) se configura desde variables de entorno.

⸻

Autenticación JWT

Ubicación:
backend/app/utils/authentication.py

Características:
	•	Firma con SECRET_KEY o JWT_SECRET
	•	Generación y validación de tokens
	•	Integración con endpoints protegidos

⸻

CORS

Configurado en backend/app/main.py.

Permite:
	•	Subdominios de Netlify mediante regex
	•	Dominios explícitos mediante variable opcional:

CORS_ALLOWED_ORIGINS=https://tu-frontend.netlify.app

Separar múltiples dominios con comas.

⸻

Endpoints Principales

Método	Endpoint	Descripción
GET	/health	Verificación de estado
POST	/auth/login	Inicio de sesión
POST	/auth/register	Registro de usuario
GET	/docs	Swagger UI
GET	/users	Lista protegida de usuarios


⸻

Deploy en Render

El proyecto incluye render.yaml en la raíz.

Render detecta automáticamente:
	•	Runtime: Python
	•	Build:

pip install -r requirements.txt


	•	Start:

uvicorn main:app --host 0.0.0.0 --port $PORT



⸻

Variables requeridas en Render

DATABASE_URL
SECRET_KEY

Después del deploy:

https://membersync-backend.onrender.com/docs


⸻

Frontend (Netlify)

Configurar variable de entorno en frontend:

VITE_API_URL=https://membersync-backend.onrender.com

Netlify realiza auto deploy al hacer push a la rama principal.

⸻

CI/CD

GitHub Actions ejecuta validaciones automáticas:

Backend:
	•	Instalación de dependencias
	•	Compilación del proyecto
	•	Verificación básica

Frontend:
	•	Instalación de dependencias
	•	Build con Vite

Si el pipeline pasa correctamente:
	•	Render realiza auto deploy del backend
	•	Netlify realiza auto deploy del frontend

⸻

Seguridad Implementada
	•	JWT firmado con clave secreta
	•	Variables sensibles fuera del repositorio
	•	CORS restringido
	•	Validación estricta con Pydantic
	•	Arquitectura async no bloqueante

⸻

Buenas Prácticas del Proyecto
	•	No subir archivo .env
	•	Usar ramas:
	•	feature/*
	•	develop
	•	main
	•	Pull Requests antes de merge
	•	Commits descriptivos
	•	No hardcodear credenciales

⸻

Checklist de Producción
	•	Variables de entorno configuradas
	•	Conexión exitosa a PostgreSQL
	•	Endpoint /health activo
	•	CORS validado
	•	Frontend apuntando a backend correcto
	•	HTTPS activo en ambos servicios

⸻

Autor

Fernando Estrada
MemberSync
2026

