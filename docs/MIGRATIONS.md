# Database Migrations Guide

## 📋 Overview

This project uses Alembic for database migrations. This guide explains how to create and run migrations both locally and in Docker.

---

## 🚀 Quick Start

### First Time Setup

1. **Create initial migration:**
   ```bash
   # Local
   alembic revision --autogenerate -m "create projects table"
   
   # Docker
   docker-compose exec api alembic revision --autogenerate -m "create projects table"
   ```

2. **Run migrations:**
   ```bash
   # Local
   alembic upgrade head
   
   # Docker
   docker-compose exec api alembic upgrade head
   
   # Using init script
   python scripts/init_db.py
   ```

3. **Seed database (optional):**
   ```bash
   python scripts/init_db.py --seed
   ```

---

## 📝 Common Commands

### Creating Migrations

**Auto-generate migration from model changes:**
```bash
# Local
alembic revision --autogenerate -m "description of changes"

# Docker
docker-compose exec api alembic revision --autogenerate -m "description of changes"
```

**Create empty migration (for manual changes):**
```bash
# Local
alembic revision -m "description"

# Docker
docker-compose exec api alembic revision -m "description"
```

### Running Migrations

**Upgrade to latest:**
```bash
# Local
alembic upgrade head

# Docker
docker-compose exec api alembic upgrade head
```

**Upgrade by one version:**
```bash
alembic upgrade +1
```

**Upgrade to specific revision:**
```bash
alembic upgrade <revision_id>
```

### Downgrading Migrations

**Downgrade by one version:**
```bash
# Local
alembic downgrade -1

# Docker
docker-compose exec api alembic downgrade -1
```

**Downgrade to specific revision:**
```bash
alembic downgrade <revision_id>
```

**Downgrade all (back to empty database):**
```bash
alembic downgrade base
```

### Viewing Migration History

**Show current revision:**
```bash
# Local
alembic current

# Docker
docker-compose exec api alembic current
```

**Show migration history:**
```bash
# Local
alembic history

# Docker
docker-compose exec api alembic history
```

**Show detailed history:**
```bash
alembic history --verbose
```

---

## 🐳 Docker-Specific Commands

### Run migrations on container startup

Add to `docker-compose.yml`:
```yaml
api:
  command: sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --reload"
```

### Access database directly

```bash
# PostgreSQL CLI
docker-compose exec db psql -U portfolio -d portfolio_db

# List tables
\dt

# Describe table
\d projects

# Exit
\q
```

---

## 🔧 Local Development

### Prerequisites

1. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Ensure database is running:**
   ```bash
   # If using Docker for DB only
   docker-compose up -d db
   ```

3. **Configure .env:**
   ```env
   DATABASE_URL=postgresql://portfolio:portfolio_dev_password@localhost:5432/portfolio_db
   ```

### Running Migrations Locally

```bash
# Create migration
alembic revision --autogenerate -m "your message"

# Review the generated migration file in alembic/versions/

# Apply migration
alembic upgrade head

# If something goes wrong, rollback
alembic downgrade -1
```

---

## 📂 Migration Files

### Location
```
alembic/
├── versions/
│   └── xxxx_create_projects_table.py  # Generated migrations
├── env.py                              # Alembic environment config
└── script.py.mako                      # Migration template
```

### Migration File Structure

```python
"""create projects table

Revision ID: xxxx
Revises: 
Create Date: 2026-02-03
"""

def upgrade() -> None:
    # Changes to apply
    op.create_table(...)

def downgrade() -> None:
    # How to revert changes
    op.drop_table(...)
```

---

## ⚠️ Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Test migrations on development database first**
3. **Never edit applied migrations** - create a new one instead
4. **Keep migrations small and focused** - one logical change per migration
5. **Write descriptive migration messages**
6. **Always provide downgrade logic** for rollback capability
7. **Backup production database** before running migrations

---

## 🐛 Troubleshooting

### "Target database is not up to date"

```bash
# Check current version
alembic current

# Check pending migrations
alembic history

# Apply pending migrations
alembic upgrade head
```

### "Can't locate revision identified by 'xxxx'"

```bash
# Stamp database with current revision
alembic stamp head

# Or stamp with specific revision
alembic stamp <revision_id>
```

### "Multiple heads detected"

```bash
# Merge migrations
alembic merge heads -m "merge migrations"
```

### Database connection errors

1. Check `.env` file has correct `DATABASE_URL`
2. Ensure database is running: `docker-compose ps`
3. Test connection: `docker-compose exec db psql -U portfolio -d portfolio_db`

---

## 🔄 Workflow Example

### Adding a new field to Project model

1. **Modify the model:**
   ```python
   # app/models/project.py
   class Project(Base):
       # ... existing fields ...
       views_count = Column(Integer, default=0)
   ```

2. **Generate migration:**
   ```bash
   alembic revision --autogenerate -m "add views_count to projects"
   ```

3. **Review migration file:**
   ```bash
   # Check alembic/versions/xxxx_add_views_count_to_projects.py
   ```

4. **Apply migration:**
   ```bash
   alembic upgrade head
   ```

5. **Verify in database:**
   ```bash
   docker-compose exec db psql -U portfolio -d portfolio_db -c "\d projects"
   ```

---

## 📚 Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [FastAPI with Alembic](https://fastapi.tiangolo.com/tutorial/sql-databases/)
