# ADR 0001: Use Django and Django REST Framework

## Status

Accepted

## Context

The project needs a backend framework that can support:

- REST APIs
- authentication
- role-based access control
- PostgreSQL
- automated testing
- integration with ML and LLM components
- clear structure for a portfolio project

## Decision

Use Python with Django and Django REST Framework for the backend.

## Why

Django provides:

- mature authentication support
- ORM for relational database access
- admin tooling
- strong project structure
- good PostgreSQL integration

Django REST Framework adds:

- API serializers
- API views/viewsets
- authentication and permission support
- REST-friendly tooling
- easier OpenAPI integration

## Alternatives Considered

- Flask
- FastAPI
- Node.js/Express

These are valid alternatives, but Django + DRF fits this project well because it provides more built-in structure for authentication, database-backed workflows, permissions, and admin functionality.

## Consequences

Positive:

- faster development of common backend features
- strong ecosystem
- good fit with PostgreSQL
- useful framework experience for backend/full-stack roles

Trade-offs:

- Django has more framework conventions to learn
- it can feel heavier than Flask or FastAPI
- some behavior is abstracted by the framework and must be understood rather than used blindly

