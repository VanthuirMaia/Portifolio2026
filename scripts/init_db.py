"""
Database initialization script.

This script initializes the database by running Alembic migrations
and optionally seeding with example data.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from alembic import command
from alembic.config import Config
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine
from app.models.project import Project


def run_migrations():
    """Run all pending Alembic migrations."""
    print("🔄 Running database migrations...")
    
    # Get alembic config
    alembic_cfg = Config("alembic.ini")
    
    # Run migrations
    command.upgrade(alembic_cfg, "head")
    
    print("✅ Migrations completed successfully!")


def seed_database():
    """Seed database with example data."""
    print("🌱 Seeding database with example data...")
    
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        existing_projects = db.query(Project).count()
        if existing_projects > 0:
            print(f"⚠️  Database already has {existing_projects} projects. Skipping seed.")
            return
        
        # Create example projects
        example_projects = [
            Project(
                title="Portfolio Website",
                slug="portfolio-website",
                short_description="Personal portfolio built with React and TypeScript",
                long_description="""
# Portfolio Website

A modern, responsive portfolio website showcasing my projects and skills.

## Features
- Responsive design
- Dark mode support
- Project filtering
- Contact form

## Tech Stack
- React 18
- TypeScript
- Tailwind CSS
- Vite
                """.strip(),
                tech_stack=["React", "TypeScript", "Tailwind CSS", "Vite"],
                project_type="web",
                status="active",
                featured=True,
                github_url="https://github.com/username/portfolio",
                demo_url="https://portfolio.example.com",
                image_url="https://via.placeholder.com/800x600"
            ),
            Project(
                title="Data Pipeline ETL",
                slug="data-pipeline-etl",
                short_description="Scalable ETL pipeline for processing large datasets",
                long_description="""
# Data Pipeline ETL

An automated ETL pipeline for extracting, transforming, and loading data from multiple sources.

## Features
- Parallel processing
- Error handling and retry logic
- Data validation
- Monitoring and alerting

## Tech Stack
- Apache Airflow
- Python
- PostgreSQL
- Docker
                """.strip(),
                tech_stack=["Python", "Apache Airflow", "PostgreSQL", "Docker", "Pandas"],
                project_type="data_engineering",
                status="active",
                featured=True,
                github_url="https://github.com/username/etl-pipeline"
            ),
            Project(
                title="ML Classification Model",
                slug="ml-classification-model",
                short_description="Machine learning model for customer churn prediction",
                long_description="""
# ML Classification Model

A machine learning model to predict customer churn with 92% accuracy.

## Features
- Feature engineering
- Model selection and tuning
- Cross-validation
- Model deployment

## Tech Stack
- Python
- Scikit-learn
- XGBoost
- MLflow
                """.strip(),
                tech_stack=["Python", "Scikit-learn", "XGBoost", "Pandas", "MLflow"],
                project_type="ml_ai",
                status="active",
                featured=False,
                github_url="https://github.com/username/ml-churn"
            ),
        ]
        
        # Add all projects
        for project in example_projects:
            db.add(project)
        
        db.commit()
        print(f"✅ Successfully seeded {len(example_projects)} example projects!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main initialization function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize database")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed database with example data"
    )
    
    args = parser.parse_args()
    
    try:
        # Run migrations
        run_migrations()
        
        # Seed if requested
        if args.seed:
            seed_database()
        
        print("\n🎉 Database initialization completed!")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
