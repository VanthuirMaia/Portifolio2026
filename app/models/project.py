"""
Project model for portfolio items.

This module defines the SQLAlchemy model for storing project information
including metadata, descriptions, tech stack, and URLs.
"""

from datetime import datetime
from typing import List

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.database import Base


class Project(Base):
    """
    Project model representing a portfolio project.
    
    Attributes:
        id: Unique identifier
        title: Project title
        slug: URL-friendly unique identifier
        short_description: Brief project summary
        long_description: Detailed markdown description
        tech_stack: List of technologies used
        project_type: Category of project
        status: Current project status
        github_url: GitHub repository URL
        demo_url: Live demo URL
        image_url: Project thumbnail/cover image
        featured: Whether project is featured on homepage
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "projects"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic Information
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    short_description = Column(String(500))
    long_description = Column(Text)  # Markdown content
    
    # Technical Details
    tech_stack = Column(ARRAY(String))  # PostgreSQL array
    project_type = Column(
        String(50),
        nullable=False,
        comment="Type: data_engineering, ml_ai, web, automation, saas"
    )
    
    # Status and Visibility
    status = Column(
        String(20),
        nullable=False,
        default="active",
        comment="Status: active, archived, draft"
    )
    featured = Column(Boolean, default=False, nullable=False)
    
    # URLs
    github_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def __repr__(self) -> str:
        """String representation of Project."""
        return (
            f"<Project(id={self.id}, "
            f"title='{self.title}', "
            f"slug='{self.slug}', "
            f"type='{self.project_type}', "
            f"status='{self.status}')>"
        )
