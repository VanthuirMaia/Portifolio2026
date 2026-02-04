"""
Project API endpoints.

This module implements REST API endpoints for managing portfolio projects.
Provides full CRUD operations with filtering, pagination, and validation.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.utils import generate_slug
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectPublic,
    ProjectUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[ProjectPublic], status_code=status.HTTP_200_OK)
def list_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    project_type: Optional[str] = Query(None, description="Filter by project type"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    featured: Optional[bool] = Query(None, description="Filter by featured flag"),
    db: Session = Depends(get_db),
) -> List[Project]:
    """
    List all projects with optional filtering and pagination.
    
    Query Parameters:
        - skip: Number of records to skip (default: 0)
        - limit: Maximum number of records to return (default: 100, max: 100)
        - project_type: Filter by project type (data_engineering, ml_ai, web, automation, saas)
        - status: Filter by status (active, archived, draft)
        - featured: Filter by featured flag (true/false)
    
    Returns:
        List of projects matching the filters
    """
    query = db.query(Project)
    
    # Apply filters
    if project_type:
        query = query.filter(Project.project_type == project_type)
    
    if status_filter:
        query = query.filter(Project.status == status_filter)
    
    if featured is not None:
        query = query.filter(Project.featured == featured)
    
    # Apply pagination and ordering
    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return projects


@router.get("/{project_id}", response_model=ProjectPublic, status_code=status.HTTP_200_OK)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> Project:
    """
    Get a specific project by ID.
    
    Args:
        project_id: The ID of the project to retrieve
    
    Returns:
        Project details
        
    Raises:
        HTTPException 404: If project not found
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    return project


@router.post("/", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
) -> Project:
    """
    Create a new project.
    
    Automatically generates a slug from the title if not provided.
    Validates that the slug is unique.
    
    Args:
        project_data: Project creation data
    
    Returns:
        Created project
        
    Raises:
        HTTPException 400: If slug already exists
    """
    # Generate slug from title if not provided or empty
    slug = project_data.slug.strip() if project_data.slug else ""
    if not slug:
        slug = generate_slug(project_data.title)
    else:
        # Normalize provided slug
        slug = generate_slug(slug)
    
    # Check if slug already exists
    existing_project = db.query(Project).filter(Project.slug == slug).first()
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with slug '{slug}' already exists"
        )
    
    # Create project instance
    project = Project(
        **project_data.model_dump(exclude={"slug"}),
        slug=slug
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project


@router.put("/{project_id}", response_model=ProjectPublic, status_code=status.HTTP_200_OK)
def update_project_full(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
) -> Project:
    """
    Fully update a project (replaces all fields).
    
    Args:
        project_id: The ID of the project to update
        project_data: Complete project data
    
    Returns:
        Updated project
        
    Raises:
        HTTPException 404: If project not found
        HTTPException 400: If slug already exists for another project
    """
    # Get existing project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    # Generate or normalize slug
    slug = project_data.slug.strip() if project_data.slug else ""
    if not slug:
        slug = generate_slug(project_data.title)
    else:
        slug = generate_slug(slug)
    
    # Check if slug already exists for another project
    if slug != project.slug:
        existing_project = db.query(Project).filter(
            Project.slug == slug,
            Project.id != project_id
        ).first()
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project with slug '{slug}' already exists"
            )
    
    # Update all fields
    for field, value in project_data.model_dump(exclude={"slug"}).items():
        setattr(project, field, value)
    
    project.slug = slug
    
    db.commit()
    db.refresh(project)
    
    return project


@router.patch("/{project_id}", response_model=ProjectPublic, status_code=status.HTTP_200_OK)
def update_project_partial(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
) -> Project:
    """
    Partially update a project (only updates provided fields).
    
    Args:
        project_id: The ID of the project to update
        project_data: Partial project data
    
    Returns:
        Updated project
        
    Raises:
        HTTPException 404: If project not found
        HTTPException 400: If slug already exists for another project
    """
    # Get existing project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    # Get only the fields that were actually provided
    update_data = project_data.model_dump(exclude_unset=True)
    
    # Handle slug if provided
    if "slug" in update_data:
        slug = update_data["slug"].strip() if update_data["slug"] else ""
        if slug:
            slug = generate_slug(slug)
            
            # Check if slug already exists for another project
            if slug != project.slug:
                existing_project = db.query(Project).filter(
                    Project.slug == slug,
                    Project.id != project_id
                ).first()
                if existing_project:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Project with slug '{slug}' already exists"
                    )
            
            update_data["slug"] = slug
    
    # Update only provided fields
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a project.
    
    Args:
        project_id: The ID of the project to delete
    
    Returns:
        No content (204)
        
    Raises:
        HTTPException 404: If project not found
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    db.delete(project)
    db.commit()
    
    return None
