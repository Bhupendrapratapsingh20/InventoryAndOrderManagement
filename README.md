# 📦 Inventory & Order Management System

A full-stack inventory and order management application built with **FastAPI** (backend), **React + Vite** (frontend), and **PostgreSQL** (database).

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Vite, React Router v7, Axios |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2 |
| **Database** | PostgreSQL 15 |
| **Containerization** | Docker, Docker Compose |
| **Deployment** | Render (Backend + DB), Vercel (Frontend) |

## 🚀 Features

- **Products Management** – Full CRUD with SKU, pricing, stock tracking, and categories
- **Customer Management** – Full CRUD with contact info and address details
- **Order Management** – Create orders with multiple items, automatic stock deduction and restoration
- **Dashboard** – Real-time stats: revenue, product count, customer count, low-stock alerts, recent orders
- **RESTful API** – Fully documented with Swagger UI (`/docs`) and ReDoc (`/redoc`)

---

## 🐳 Docker Setup (Local Development)

### Prerequisites
- Docker & Docker Compose installed

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd inventoryAndOrderManagement
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred values
   ```

3. **Start all services:**
   ```bash
   docker-compose up -d --build
   ```

4. **Access the application:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health Check: [http://localhost:8000/health](http://localhost:8000/health)

### Docker Services

| Service | Container | Port | Image |
|---------|-----------|------|-------|
| PostgreSQL | `inventory_db` | 5432 | `postgres:15-alpine` |
| FastAPI Backend | `inventory_api` | 8000 | `python:3.11-slim` (multi-stage) |
| React Frontend | `inventory_web` | 3000 | `node:20-alpine` + `nginx:alpine` (multi-stage) |

### Docker Features
- ✅ Multi-stage builds with slim/lightweight base images
- ✅ Named volumes for PostgreSQL data persistence (`postgres_data`)
- ✅ No hardcoded credentials (all via environment variables)
- ✅ Health checks on all services
- ✅ Production-ready Dockerfiles
- ✅ `.dockerignore` files for both backend and frontend
- ✅ Internal Docker network for service communication

---

## ☁️ Deployment

### Backend → Render

1. **Push to GitHub** and connect the repo to [Render](https://render.com)

2. **Create a PostgreSQL database** on Render:
   - Go to Render Dashboard → **New** → **PostgreSQL**
   - Name: `inventory-db`
   - Plan: Free
   - Save the **Internal Database URL**

3. **Create a Web Service** on Render:
   - Go to Render Dashboard → **New** → **Web Service**
   - Connect your GitHub repo
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Docker Command**: _(leave default)_
   - **Plan**: Free

4. **Set environment variables** on Render:
   | Variable | Value |
   |----------|-------|
   | `DATABASE_URL` | _(paste Internal Database URL from step 2)_ |
   | `SECRET_KEY` | _(generate a random string)_ |
   | `DEBUG` | `false` |
   | `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` |
   | `APP_NAME` | `Inventory & Order Management API` |
   | `API_V1_PREFIX` | `/api/v1` |

   > **Important:** Render gives you a `postgres://` URL. The app automatically converts it to `postgresql+asyncpg://` for the async driver.

5. Deploy and note your backend URL (e.g., `https://inventory-api-xxxx.onrender.com`)

### Frontend → Vercel

1. Go to [Vercel](https://vercel.com) and import your GitHub repo

2. **Configure the project:**
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

3. **Set environment variable:**
   | Variable | Value |
   |----------|-------|
   | `VITE_API_BASE_URL` | `https://inventory-api-xxxx.onrender.com` _(your Render backend URL)_ |

4. Deploy!

5. **Update Render's `ALLOWED_ORIGINS`** with your Vercel URL:
   ```
   https://your-app.vercel.app
   ```

---

## 📁 Project Structure

```
inventoryAndOrderManagement/
├── docker-compose.yml          # Orchestrates all 3 services
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── render.yaml                 # Render.com deployment blueprint
│
├── backend/
│   ├── Dockerfile              # Multi-stage Python build
│   ├── .dockerignore           # Docker build exclusions
│   ├── requirements.txt        # Python dependencies
│   ├── prestart.sh             # Pre-start migration script
│   ├── alembic.ini             # Alembic config
│   ├── alembic/                # Database migrations
│   │   └── versions/           # Migration files
│   └── app/
│       ├── main.py             # FastAPI application entry
│       ├── config.py           # Settings from env vars
│       ├── database.py         # Async DB engine & session
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic request/response schemas
│       ├── crud/               # Database operations
│       └── routers/            # API route handlers
│
└── frontend/
    ├── Dockerfile              # Multi-stage Node + Nginx build
    ├── .dockerignore           # Docker build exclusions
    ├── vercel.json             # Vercel deployment config
    ├── nginx.conf              # Nginx config (Docker)
    ├── package.json            # Node dependencies
    └── src/
        ├── App.jsx             # Root component with routing
        ├── main.jsx            # React entry point
        ├── api/                # Axios API client
        ├── pages/              # Page components
        ├── hooks/              # Custom React hooks
        ├── context/            # React context providers
        ├── components/         # Reusable UI components
        └── styles/             # CSS stylesheets
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/products/` | List products |
| POST | `/api/v1/products/` | Create product |
| GET | `/api/v1/products/{id}` | Get product |
| PUT | `/api/v1/products/{id}` | Update product |
| DELETE | `/api/v1/products/{id}` | Delete product |
| GET | `/api/v1/customers/` | List customers |
| POST | `/api/v1/customers/` | Create customer |
| GET | `/api/v1/customers/{id}` | Get customer |
| PUT | `/api/v1/customers/{id}` | Update customer |
| DELETE | `/api/v1/customers/{id}` | Delete customer |
| GET | `/api/v1/orders/` | List orders |
| POST | `/api/v1/orders/` | Create order |
| GET | `/api/v1/orders/{id}` | Get order |
| DELETE | `/api/v1/orders/{id}` | Delete order |
| GET | `/api/v1/dashboard/stats` | Dashboard statistics |

---

## 🔐 Environment Variables

All configuration is done through environment variables. No credentials are hardcoded.

See `.env.example` for the full list of required variables.
