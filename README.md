# Portfolio API

> Professional FastAPI backend for portfolio management with complete CRUD operations, PostgreSQL database, and Docker support.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Development](#-development)
- [Documentation](#-documentation)

## ✨ Features

- **Complete REST API** - Full CRUD operations for projects
- **PostgreSQL Database** - Production-ready database with SQLAlchemy ORM
- **Docker Support** - Complete containerization with docker-compose
- **Type Safety** - Full type hints with Pydantic v2
- **Auto Documentation** - Interactive API docs with Swagger UI
- **Data Validation** - Request/response validation with Pydantic schemas
- **Filtering & Pagination** - Query parameters for list endpoints
- **Health Checks** - Container and application health monitoring
- **Database Migrations** - Alembic for schema version control

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | FastAPI 0.115.0 |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.0.35 |
| **Validation** | Pydantic 2.5.2 |
| **Migrations** | Alembic 1.13.3 |
| **Container** | Docker & Docker Compose |

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd portfolio-api

# Setup environment
cp .env.example .env

# Start services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head

# (Optional) Seed database
docker-compose exec api python scripts/init_db.py --seed
```

**Access the API:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## 📚 API Endpoints

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/projects` | List all projects (with filters) |
| `GET` | `/api/v1/projects/{id}` | Get project by ID |
| `POST` | `/api/v1/projects` | Create new project |
| `PUT` | `/api/v1/projects/{id}` | Update project (full) |
| `PATCH` | `/api/v1/projects/{id}` | Update project (partial) |
| `DELETE` | `/api/v1/projects/{id}` | Delete project |

**Query Parameters (GET /projects):**
- `skip` - Number of records to skip (pagination)
- `limit` - Maximum records to return (max: 100)
- `project_type` - Filter by type (data_engineering, ml_ai, web, automation, saas)
- `status` - Filter by status (active, archived, draft)
- `featured` - Filter by featured flag (true/false)

## 🔧 Development

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# In Docker
docker-compose exec api alembic upgrade head
```

See [docs/MIGRATIONS.md](docs/MIGRATIONS.md) for complete guide.

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Access database
docker-compose exec db psql -U portfolio -d portfolio_db
```

### With pgAdmin (Optional)

```bash
# Copy override example
cp docker-compose.override.yml.example docker-compose.override.yml

# Start with pgAdmin
docker-compose up -d
```

Access pgAdmin at http://localhost:5050
- Email: `admin@portfolio.local`
- Password: `admin`

## 📖 Documentation

- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/api/v1/openapi.json
- **Migrations Guide:** [docs/MIGRATIONS.md](docs/MIGRATIONS.md)

## 📝 Environment Variables

See `.env.example` for all configuration options.

**Key Variables:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db
SECRET_KEY=your-secret-key-here
DEBUG=False
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/

# In Docker
docker-compose exec api pytest
```

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using FastAPI**
