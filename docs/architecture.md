# Architecture

## AI-Assisted Support Ops Platform

**Document status:** Initial Phase 0 architecture
**Purpose:** Describe how the major parts of the system are organized and how they interact.

> This document explains the high-level technical structure of the system. Detailed database design belongs in `erd.md`, and detailed requirements belong in `srs.md`.

---

## 1. Architecture Goals

The architecture should support:

* clear separation between frontend, backend, database, and AI components
* secure user authentication and authorization
* testable business logic
* auditable AI decisions
* human approval for customer-facing AI output
* gradual growth without unnecessary early complexity
* deployment through containers
* later monitoring, load testing, and local Kubernetes practice

The architecture should remain understandable enough that each major component can be explained independently.

---

## 2. High-Level Architecture

The system will use a layered web architecture.

```
Customer / Support Agent / Admin
              |
              v
          Frontend
              |
              | HTTP / REST
              v
     Django REST Framework API
              |
     +--------+--------+
     |                 |
     v                 v
Business Logic     Auth / RBAC
     |
     +-------------------------------+
     |               |               |
     v               v               v
PostgreSQL       ML Components     LLM Component
     |               |               |
     |               |               v
     |               |        Suggested Response
     |               |               |
     |               +---------------+
     |                               |
     v                               v
Persistent Data                Human Review
                                     |
                                     v
                                 Approval
                                     |
                                     v
                                  Audit Log
```

Main idea:

```
Frontend
    ↓
API
    ↓
Business logic
    ↓
Database / AI services
```

The frontend should not directly access the database or ML/LLM components.

---

## 3. Main Components

### 3.1 Frontend

The frontend is the user-facing part of the application.

It will provide interfaces for:

* Customers
* Support Agents
* Admins

Examples:

```
Customer
→ creates ticket
→ views ticket status

Support Agent
→ views assigned tickets
→ reviews AI suggestions
→ approves responses

Admin
→ manages users
→ reviews audit/evaluation data
```

The frontend will communicate with the backend through HTTP requests to REST API endpoints.

The exact frontend framework does not need to be fixed during Phase 0.

A JavaScript-based frontend will be selected later.

---

## 3.2 Django REST API

The Django REST API will be the main backend interface.

Technology:

* Python
* Django
* Django REST Framework

Responsibilities include:

* receiving frontend requests
* validating requests
* authenticating users
* checking permissions
* managing tickets
* managing assignments
* executing business rules
* communicating with PostgreSQL
* calling ML components
* calling LLM-related services
* returning API responses

Example:

```
Frontend sends:

POST /api/tickets/

        ↓

Django REST API validates request

        ↓

Ticket business logic runs

        ↓

Ticket stored in PostgreSQL

        ↓

API returns response to frontend
```

---

## 3.3 Business Logic Layer

Business logic defines the rules of the system.

Examples:

* who may access a ticket
* whether a ticket can move to a certain status
* when assignment is allowed
* when AI generation is allowed
* whether a response can be approved
* what must be written to the audit log

This logic should not be unnecessarily mixed into frontend code.

Example:

```
Support Agent attempts to approve response

        ↓

Backend checks:

Is user authenticated?
Is user an AGENT?
Is this ticket assigned appropriately?
Does a draft exist?

        ↓

If valid → approve

Otherwise → reject request
```

Keeping this logic in the backend makes the behavior more secure and testable.

---

## 3.4 PostgreSQL Database

PostgreSQL will be the main relational database.

It will store persistent application data such as:

* users
* tickets
* assignments
* AI predictions
* suggested responses
* audit records

Example:

```
Django application
      |
      v
  PostgreSQL
      |
      +--> USER
      +--> TICKET
      +--> ASSIGNMENT
      +--> AI_PREDICTION
      +--> SUGGESTED_RESPONSE
      +--> AUDIT_LOG
```

Detailed relationships are documented in:

`docs/erd.md`

---

## 3.5 Authentication and Role-Based Access Control

Authentication answers:

> Who is this user?

Authorization answers:

> What is this user allowed to do?

Initial roles:

* CUSTOMER
* AGENT
* ADMIN

Example:

```
Customer
→ may create ticket
→ may view own tickets

Agent
→ may handle assigned tickets
→ may review and approve responses

Admin
→ may access administrative functionality
```

Permissions will be enforced primarily by the backend API.

The frontend may hide unauthorized controls, but frontend hiding alone is not considered security.

---

## 3.6 ML Components

Machine learning components will initially handle:

* ticket classification
* priority prediction

Example:

```
Ticket:
"I was charged twice for the same payment."

        ↓

Classification model

        ↓

category = BILLING

        ↓

Priority model

        ↓

priority = HIGH
```

The prediction should include metadata such as:

* predicted value
* confidence score
* model version
* timestamp

Predictions should be stored so they can later be evaluated against human decisions.

---

## 3.7 Routing Component

Routing decides which support agent or team should receive a ticket.

Inputs may include:

* category
* priority
* routing rules
* agent/team responsibility

Initial routing should remain simple.

Example:

```
category = BILLING
      |
      v
Billing routing rule
      |
      v
Billing support agent
```

A more advanced ML-based routing system is not required initially.

---

## 3.8 LLM Component

The LLM component will generate suggested customer responses.

Example:

```
Ticket + relevant context
         |
         v
        LLM
         |
         v
   Suggested draft
```

The LLM should not directly send customer-facing responses.

Its output is treated as a suggestion.

---

## 3.9 Human Approval Workflow

Human approval is a core architectural constraint.

The workflow is:

```
LLM generates response
        |
        v
Suggested response stored
        |
        v
Support Agent reviews
      /      \
     /        \
  Edit        Accept
     \        /
      \      /
       v    v
     Human approval
          |
          v
     Final response
```

The architecture must prevent an unapproved AI-generated response from becoming a final customer response.

---

## 3.10 Audit Logging

The audit component records important system actions.

Examples:

* ticket creation
* classification
* priority prediction
* assignment
* reassignment
* AI response generation
* human edits
* approval
* ticket resolution

Example:

```
10:00 TICKET_CREATED
10:01 AI_CLASSIFIED
10:02 PRIORITY_PREDICTED
10:03 AGENT_ASSIGNED
10:15 RESPONSE_GENERATED
10:20 RESPONSE_EDITED
10:22 RESPONSE_APPROVED
```

Audit logging supports:

* traceability
* debugging
* evaluation
* accountability
* understanding AI/human interaction

---

## 4. High-Level Data Flow

A normal ticket workflow:

```
1. Customer submits ticket

2. Frontend sends request to Django REST API

3. API validates request

4. Ticket is stored in PostgreSQL

5. ML component classifies ticket

6. ML component predicts priority

7. Prediction results are stored

8. Routing logic creates an assignment

9. Support Agent views ticket

10. LLM generates suggested response

11. Suggested response is stored

12. Agent reviews or edits response

13. Agent approves response

14. Final state is stored

15. Important actions are added to the audit log
```

---

## 5. Request Flow Example

Example: Customer creates a ticket.

```
Browser
   |
   | POST /api/tickets/
   v
Django REST Framework
   |
   | validate input
   | check authentication
   v
Ticket business logic
   |
   v
PostgreSQL
   |
   v
Ticket stored
```

Later:

```
Stored Ticket
    |
    +--> ML classification
    |
    +--> Priority prediction
    |
    +--> Routing
    |
    +--> Audit logging
```

---

## 6. AI Processing Flow

```
Ticket text
    |
    v
ML Classification
    |
    +--> predicted category
    |
    v
Priority Prediction
    |
    +--> predicted priority
    |
    v
Store predictions
    |
    v
Routing logic
    |
    v
Support Agent
```

For response generation:

```
Ticket
  +
relevant context
    |
    v
   LLM
    |
    v
Suggested Response
    |
    v
Human Review
    |
    v
Approved Response
```

---

## 7. Architectural Principles

### 7.1 Separation of Concerns

Different responsibilities should remain separated.

Examples:

* frontend handles presentation
* API handles external requests
* business logic handles system rules
* database handles persistence
* ML handles predictions
* LLM handles response suggestions

This improves:

* readability
* testing
* maintainability
* debugging

---

### 7.2 API-First Communication

The frontend should communicate with the backend through REST APIs.

This means the backend can be developed and tested independently from the frontend.

Example:

```
Frontend
   |
   | JSON over HTTP
   v
REST API
   |
   v
Backend
```

---

### 7.3 Human-in-the-Loop AI

Customer-facing AI output requires human approval.

Principle:

```
AI proposes
Human decides
System records
```

---

### 7.4 Auditability

Important AI and human actions should remain traceable.

We should be able to determine:

* what the AI predicted
* which model version produced it
* whether a human changed it
* who approved a response
* when important actions occurred

---

### 7.5 Testability

Important business logic should be designed so it can be tested automatically.

Examples:

* customer cannot view another customer's ticket
* unapproved response cannot become final
* reassignment preserves history
* AI failure does not delete or block the ticket

---

### 7.6 Incremental Complexity

The architecture should start simple.

Example:

```
Start:
rule-based routing

Later if justified:
more advanced routing
```

We should not introduce complex infrastructure before there is a learning or technical reason for it.

---

### 7.7 AI Is Not a Dependency for Core Availability

The core ticket system should continue functioning if AI services fail.

Example:

```
AI service unavailable
        |
        v
Ticket still exists
        |
        v
Human agent can handle ticket manually
```

---

## 8. Initial Technology Stack

### Backend

* Python
* Django
* Django REST Framework

Why:

* mature web framework
* strong ORM
* built-in authentication support
* strong ecosystem
* useful for backend/full-stack job preparation

---

### Database

* PostgreSQL

Why:

* relational database
* strong data integrity
* widely used in production web systems
* works well with Django

---

### Frontend

* JavaScript-based frontend

The specific framework will be selected later.

Potential options may include:

* React
* another appropriate JavaScript frontend framework

The choice should be made based on project needs rather than choosing complexity for its own sake.

---

### Testing

* pytest
* pytest-django where appropriate

Testing will cover:

* business logic
* API behavior
* permissions
* AI workflow
* audit behavior

---

### Containers

* Docker
* Docker Compose where appropriate

Purpose:

* reproducible development environment
* isolated services
* easier PostgreSQL setup
* deployment preparation

---

### CI/CD

* GitHub Actions

Initial CI flow:

```
git push
    |
    v
GitHub Actions
    |
    +--> install dependencies
    +--> run tests
    +--> run checks
    +--> report result
```

Deployment automation will be introduced later.

---

### Machine Learning

Python-based ML tools will be used for:

* ticket classification
* priority prediction

The exact libraries and models will be selected during the ML phase.

---

### LLM Integration

The project will integrate an LLM through an API.

Later functionality may include:

* response drafting
* controlled tool calling
* retrieval of relevant support information

The LLM will remain behind human approval controls.

---

### Monitoring

Planned tools:

* Prometheus
* Grafana

Prometheus will collect metrics.

Grafana will visualize them.

Examples:

* request rate
* response time
* error rate
* application health
* resource usage

---

### Load Testing

Planned options:

* k6
* Locust

One tool will be selected later.

Purpose:

* simulate multiple users
* measure API performance
* identify bottlenecks
* observe behavior under load

---

### Kubernetes

Planned learning environment:

* kind
* or minikube

Kubernetes will be used locally to learn:

* pods
* deployments
* services
* scaling concepts
* container orchestration

This project will **not** describe the local Kubernetes setup as production-grade infrastructure.

---

## 9. Development and Deployment Evolution

The project should evolve gradually.

```
Local development
      |
      v
Django + PostgreSQL
      |
      v
Automated tests
      |
      v
Docker
      |
      v
GitHub Actions
      |
      v
Cloud deployment
      |
      v
Monitoring
      |
      v
Local Kubernetes
      |
      v
Load testing
```

Each infrastructure step should be introduced only after the previous application layer is understood.

---

## 10. Failure Handling

### Database Failure

If the database is unavailable, API operations requiring persistent data should fail clearly rather than pretending they succeeded.

---

### ML Failure

If classification or priority prediction fails:

```
Ticket remains stored
    |
    v
Prediction failure recorded
    |
    v
Human handling remains possible
```

---

### LLM Failure

If response generation fails:

```
Ticket remains usable
    |
    v
Agent may continue manually
```

The system should not depend on the LLM for core support functionality.

---

### Authorization Failure

If a user attempts an unauthorized action:

```
Request
   |
   v
Permission check
   |
   v
Access denied
```

The backend must enforce this rule even if the frontend accidentally exposes a control.

---

## 11. Security Boundaries

The frontend is not trusted to enforce permissions.

Security should primarily be enforced by the backend.

```
User
  |
  v
Frontend
  |
  v
Django REST API
  |
  +--> authentication
  |
  +--> authorization
  |
  v
protected business logic
```

Sensitive credentials such as API keys must not be committed to Git.

Environment variables or appropriate secret-management mechanisms should be used.

---

## 12. Relationship to Other Documents

Project documentation:

```
docs/
├── srs.md
├── architecture.md
├── erd.md
└── adr/
```

### `srs.md`

Defines:

> What must the system do?

### `architecture.md`

Defines:

> How are the major parts of the system organized?

### `erd.md`

Defines:

> How is persistent data structured?

### `adr/`

Defines:

> Why were important technical decisions made?

---

## 13. Architecture Decision Records

Major decisions should later receive an ADR when the reasoning matters.

Examples:

* Why Django instead of another backend framework?
* Why PostgreSQL?
* Why REST?
* Why preserve assignment history?
* Why require human approval?
* Why store AI prediction history?
* Why use Docker?
* Why use local Kubernetes only as a learning environment?

An ADR should usually contain:

```
Context
↓
Options considered
↓
Decision
↓
Consequences
```

---

## 14. Initial Architecture Summary

The system can be summarized as:

```
Users
  |
  v
Frontend
  |
  v
Django REST API
  |
  +--------------------+
  |                    |
  v                    v
Business Logic     Authentication / RBAC
  |
  +----------+-----------+-----------+
  |          |           |           |
  v          v           v           v
PostgreSQL   ML       Routing       LLM
  |          |                       |
  |          v                       v
  |      Predictions           Suggested Response
  |                                  |
  |                                  v
  |                            Human Approval
  |                                  |
  +----------------+-----------------+
                   |
                   v
               Audit Log
```

The architectural idea is:

```
Core web application first
        |
        v
AI assistance second
        |
        v
human control always
        |
        v
audit everything important
```

---

## 15. Current Status

This architecture belongs to **Phase 0 — Planning**.

At this stage:

* requirements are defined in `srs.md`
* initial database relationships are defined in `erd.md`
* the high-level architecture is defined here
* ADRs will document important technology decisions

Implementation has not yet started.

The architecture will be refined as the system is built, tested, and deployed.

Changes should be intentional and documented rather than silently diverging from the planned architecture.
