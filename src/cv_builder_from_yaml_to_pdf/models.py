"""CV Builder data models using Pydantic.

This module defines the data models for CV builder using Pydantic for validation.
"""

from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class PersonalInfo(BaseModel):
    """Model for personal information section."""
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None
    title: Optional[str] = None


class Education(BaseModel):
    """Model for education entries."""
    institution: str
    degree: str
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = None
    details: Optional[str] = None
    gpa: Optional[str] = None


class Experience(BaseModel):
    """Model for professional experience entries."""
    company: str
    title: str
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    achievements: Optional[List[str]] = None


class Skill(BaseModel):
    """Model for skills section."""
    category: str
    name: str


class Project(BaseModel):
    """Model for projects section."""
    name: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    link: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    achievements: Optional[List[str]] = None


class Certificate(BaseModel):
    """Model for certifications section."""
    name: str
    issuer: str
    date: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None


class Language(BaseModel):
    """Model for language proficiency."""
    name: str
    proficiency: str


class Reference(BaseModel):
    """Model for professional references."""
    name: str
    position: str
    company: str
    contact: Optional[str] = None
    relation: Optional[str] = None


class CV(BaseModel):
    """Main CV model that contains all sections."""
    personal_info: PersonalInfo
    education: List[Education]
    experience: List[Experience]
    skills: Optional[List[Skill]] = None
    projects: Optional[List[Project]] = None
    certifications: Optional[List[Certificate]] = None
    languages: Optional[List[Language]] = None
    references: Optional[List[Reference]] = None
    publications: Optional[List[str]] = None
    awards: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    custom_sections: Optional[dict] = None
