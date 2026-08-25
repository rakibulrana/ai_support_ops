# Architecture

## 1. Overview

The system will use a layered web architecture with a Django REST API, PostgreSQL database, AI/ML components, and a human approval workflow.

## 2. Main Components

- Frontend
- Django REST API
- PostgreSQL database
- ML classification and priority prediction
- LLM response generation
- Human approval workflow
- Audit logging     = records important system and AI actions.



## 3. High-Level Data Flow

Customer submits ticket

→ Django REST API receives it

→ Ticket is stored in PostgreSQL

→ ML classifies the ticket and predicts priority

→ Routing logic assigns it to a support agent

→ LLM generates a suggested response

→ Support agent reviews or edits it

→ Support agent approves the final response

→ Important actions are stored in the audit log



## 4. Architectural Principles

- Separate frontend, backend, database, and AI responsibilities
- Keep customer-facing AI responses under human approval
- Use role-based access control
- Log important AI and human actions
- Test important system behavior
- Avoid unnecessary complexity early


## 5. Initial Technology Choices

- Backend: Python, Django, Django REST Framework
- Database: PostgreSQL
- Frontend: JavaScript-based frontend
- Testing: pytest
- Containers: Docker
- CI/CD: GitHub Actions
- ML: Python-based classification and priority prediction
- LLM integration: API-based LLM
- Monitoring: Prometheus and Grafana
- Load testing: k6 or Locust
- Kubernetes: local learning setup with kind or minikube

