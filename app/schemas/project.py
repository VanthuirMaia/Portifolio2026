"""
Project schemas for request/response validation.

This module defines Pydantic schemas for Project entity validation,
serialization, and documentation in API endpoints.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectBase(BaseModel):
    """
    Base schema with shared project attributes.
    
    Used as a foundation for other project schemas.
    """
    
    title: str = Field(..., min_length=1, max_length=200, description="Project title")
    slug: str = Field(..., min_length=1, max_length=200, description="URL-friendly identifier")
    short_description: Optional[str] = Field(None, max_length=500, description="Brief summary")
    long_description: Optional[str] = Field(None, description="Detailed markdown description")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies used")
    project_type: str = Field(
        ...,
        pattern="^(data_engineering|ml_ai|web|automation|saas)$",
        description="Project category"
    )
    status: str = Field(
        default="active",
        pattern="^(active|archived|draft)$",
        description="Project status"
    )
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub repository URL")
    demo_url: Optional[str] = Field(None, max_length=500, description="Live demo URL")
    image_url: Optional[str] = Field(None, max_length=500, description="Project image URL")
    featured: bool = Field(default=False, description="Featured on homepage")


class ProjectCreate(ProjectBase):
    """
    Schema for creating a new project.
    
    Excludes auto-generated fields like id and timestamps.
    """
    
    pass


class ProjectUpdate(BaseModel):
    """
    Schema for updating an existing project.
    
    All fields are optional to support partial updates.
    """
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    short_description: Optional[str] = Field(None, max_length=500)
    long_description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    project_type: Optional[str] = Field(
        None,
        pattern="^(data_engineering|ml_ai|web|automation|saas)$"
    )
    status: Optional[str] = Field(
        None,
        pattern="^(active|archived|draft)$"
    )
    github_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    featured: Optional[bool] = None


class ProjectInDB(ProjectBase):
    """
    Schema representing a project as stored in database.
    
    Includes all fields including auto-generated ones.
    """
    
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class ProjectPublic(ProjectInDB):
    """
    Schema for public project responses.
    
    This is what gets returned to API consumers.
    Currently identical to ProjectInDB, but separated for future flexibility
    (e.g., if we need to hide certain fields from public view).
    """
    
    pass


class ProjectListResponse(BaseModel):
    """
    Schema for paginated list of projects.
    """
    
    total: int = Field(..., description="Total number of projects")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    projects: List[ProjectPublic] = Field(..., description="List of projects")
    
    model_config = ConfigDict(from_attributes=True)
