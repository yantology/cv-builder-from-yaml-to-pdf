# CV Schema Documentation

This document describes the schema for the CV data used by CV Builder.

## CV Schema

### personal_info (required)

**Type**: `PersonalInfo`

### education (required)

**Type**: `array`

### experience (required)

**Type**: `array`

### skills

### projects

### certifications

### languages

### references

### publications

### awards

### interests

### custom_sections


## Model Definitions

### Certificate

Model for certifications section.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes |  |
| issuer | string | Yes |  |
| date | Any | No |  |
| description | Any | No |  |
| link | Any | No |  |

### Education

Model for education entries.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| institution | string | Yes |  |
| degree | string | Yes |  |
| start_date | string | Yes |  |
| end_date | Any | No |  |
| location | Any | No |  |
| details | Any | No |  |
| gpa | Any | No |  |

### Experience

Model for professional experience entries.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| company | string | Yes |  |
| title | string | Yes |  |
| start_date | string | Yes |  |
| end_date | Any | No |  |
| location | Any | No |  |
| description | Any | No |  |
| achievements | Any | No |  |

### Language

Model for language proficiency.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes |  |
| proficiency | string | Yes |  |

### PersonalInfo

Model for personal information section.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes |  |
| email | string | Yes |  |
| phone | Any | No |  |
| location | Any | No |  |
| website | Any | No |  |
| linkedin | Any | No |  |
| github | Any | No |  |
| summary | Any | No |  |
| title | Any | No |  |

### Project

Model for projects section.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes |  |
| description | Any | No |  |
| technologies | Any | No |  |
| link | Any | No |  |
| start_date | Any | No |  |
| end_date | Any | No |  |
| achievements | Any | No |  |

### Reference

Model for professional references.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes |  |
| position | string | Yes |  |
| company | string | Yes |  |
| contact | Any | No |  |
| relation | Any | No |  |

### Skill

Model for skills section.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| category | string | Yes |  |
| name | string | Yes |  |

