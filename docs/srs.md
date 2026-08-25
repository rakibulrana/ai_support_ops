# Software Requirements Specification

## AI-Assisted Support Ops Platform

**Document status:** Initial Phase 0 specification
**Purpose:** Define what the system must do before implementation begins.

> This document focuses on system requirements. Detailed technical design belongs mainly in `architecture.md`, while database structure belongs in `erd.md`.

---

## 1. Purpose

The AI-Assisted Support Ops Platform is a support-ticket system that assists support teams with:

* classifying incoming tickets
* predicting ticket priority
* routing tickets to appropriate support agents
* generating suggested customer responses
* requiring human review before customer-facing AI-generated responses are sent
* recording AI decisions, human edits, approvals, and overrides for auditing and evaluation

The system is **AI-assisted, not fully autonomous**.

Core principle:

```
AI proposes
→ Human decides
→ System records
```

---

## 2. Scope

The system will include:

* user authentication
* role-based access control
* ticket creation and management
* ticket status tracking
* ticket classification
* priority prediction
* ticket assignment and reassignment
* assignment history
* AI-generated response suggestions
* human editing and approval
* audit logging
* AI/ML evaluation
* REST API
* API documentation
* automated testing
* containerized deployment
* continuous integration
* monitoring
* load testing

The project is primarily a portfolio and learning project designed to demonstrate full-stack, backend, database, AI/ML, testing, and DevOps skills.

---

## 3. System Actors

### 3.1 Customer

A Customer is a user who submits support requests.

A Customer can:

* create support tickets
* view their own tickets
* view ticket status
* view final responses related to their tickets

A Customer cannot:

* view another customer's private tickets
* assign tickets
* approve AI-generated responses
* access administrative functions

---

### 3.2 Support Agent

A Support Agent is an employee who handles support tickets.

A Support Agent can:

* view tickets assigned to them
* update ticket status
* review ticket category and priority
* review AI predictions
* review AI-generated response suggestions
* edit suggested responses
* approve responses
* participate in ticket reassignment when authorized

---

### 3.3 Admin

An Admin manages system-level functionality.

An Admin can:

* manage users
* manage roles
* review assignments
* manage routing configuration
* inspect audit logs
* review AI evaluation data
* access administrative information

---

## 4. High-Level System Workflow

```
Customer creates ticket
        |
        v
   Ticket stored
        |
        v
ML classifies ticket
        |
        v
ML predicts priority
        |
        v
Routing assigns ticket
        |
        v
Support agent reviews
        |
        v
LLM generates draft
        |
        v
Agent reviews / edits
        |
        v
    Approved?
     /     \
   No       Yes
   |         |
   +---------+----> Final response
                      |
                      v
               Audit information stored
```

Important rule:

```
AI-generated response
        !=
automatically sent response
```

A human must approve customer-facing AI-generated content.

---

## 5. Ticket Lifecycle

Initial ticket states:

```
NEW
 |
 v
CLASSIFIED
 |
 v
ASSIGNED
 |
 v
IN_PROGRESS
 |
 v
WAITING_FOR_APPROVAL
 |
 v
RESOLVED
```

### NEW

The ticket has been created.

### CLASSIFIED

The system has produced category and priority predictions.

### ASSIGNED

The ticket has been assigned to a support agent.

### IN_PROGRESS

A support agent is actively handling the ticket.

### WAITING_FOR_APPROVAL

A suggested response exists and requires human review.

### RESOLVED

The support issue has been completed.

> The lifecycle may later be refined if implementation reveals additional required states.

---

# 6. Functional Requirements

Functional requirements describe **what the system must do**.

Identifiers such as `FR-001` allow requirements to be referenced later in implementation, testing, documentation, and interviews.

---

## 6.1 Authentication and Authorization

### FR-001 — User Authentication

The system shall require authentication for protected functionality.

---

### FR-002 — Role-Based Access Control

The system shall initially support these roles:

* `CUSTOMER`
* `AGENT`
* `ADMIN`

Permissions shall depend on the user's role.

---

### FR-003 — Resource Access

Customers shall only be able to access tickets and resources they are authorized to view.

Example:

```
Alice creates Ticket 101.
Bob is another customer.

Bob must not be able to access Ticket 101.
```

---

## 6.2 Ticket Management

### FR-004 — Create Ticket

An authenticated Customer shall be able to create a support ticket.

A ticket shall contain at least:

* title
* description
* creator
* status
* creation timestamp

---

### FR-005 — View Own Tickets

Customers shall be able to view tickets they created.

---

### FR-006 — View Assigned Tickets

Support Agents shall be able to view tickets assigned to them.

---

### FR-007 — Update Ticket Status

Authorized Support Agents shall be able to update the status of tickets they are permitted to handle.

---

## 6.3 Classification and Priority Prediction

### FR-008 — Ticket Classification

The system shall classify tickets into predefined categories.

Initial examples may include:

* `BILLING`
* `TECHNICAL`
* `ACCOUNT`
* `GENERAL`

The category list may evolve during implementation.

---

### FR-009 — Priority Prediction

The system shall predict a priority level for tickets.

Initial priority levels:

* `LOW`
* `MEDIUM`
* `HIGH`

---

### FR-010 — Prediction Metadata

The system shall store relevant prediction information, including:

* predicted value
* model version
* confidence score
* prediction timestamp

---

### FR-011 — Prediction History

The system shall support storing multiple predictions for the same ticket.

This supports:

* model reruns
* model upgrades
* evaluation
* comparison between model versions

Example:

```
Ticket 101

Model v1 → HIGH
Model v2 → MEDIUM
Human final decision → HIGH
```

The system should preserve the original predictions rather than overwriting them.

---

## 6.4 Ticket Routing and Assignment

### FR-012 — Ticket Assignment

The system shall support assigning a ticket to a Support Agent.

---

### FR-013 — Ticket Reassignment

The system shall support moving a ticket from one agent to another when required.

---

### FR-014 — Assignment History

The system shall preserve assignment history.

Example:

```
Ticket 101

10:00 → assigned to Alice
11:30 → reassigned to Bob
```

Alice's previous assignment must remain recorded after Bob receives the ticket.

---

### FR-015 — Routing Logic

The system shall support routing tickets using information such as:

* predicted category
* priority
* team or agent responsibility
* configured routing rules

The first implementation may use simple rule-based routing.

More advanced routing is not required initially.

---

## 6.5 AI-Generated Response Workflow

### FR-016 — Generate Suggested Response

The system shall allow an LLM to generate a suggested response for a support ticket.

The generated response shall be treated as a draft.

---

### FR-017 — Human Review

A Support Agent shall be able to review an AI-generated response.

The agent may:

* accept it
* edit it
* reject it
* request another suggestion

---

### FR-018 — Human Approval

A customer-facing AI-generated response shall require human approval.

The system shall not treat an unapproved AI-generated response as final customer communication.

---

### FR-019 — Preserve Generated and Edited Text

The system should preserve:

* the original AI-generated response
* the human-edited response, when changes are made

This allows later evaluation of how much agents modify AI suggestions.

Example:

```
AI generated:
"Your payment problem has been received."

Agent edited:
"We have received your payment issue and are reviewing the duplicate charge."
```

Both versions should remain available for evaluation.

---

## 6.6 Audit Logging

### FR-020 — Audit Important Actions

The system shall record important actions.

Examples:

```
TICKET_CREATED
AI_CLASSIFIED
PRIORITY_PREDICTED
AGENT_ASSIGNED
AGENT_REASSIGNED
RESPONSE_GENERATED
RESPONSE_EDITED
RESPONSE_APPROVED
TICKET_RESOLVED
```

---

### FR-021 — Record Actor

When a human performs an action, the audit record shall identify the responsible user.

Example:

```
action = RESPONSE_APPROVED
user = Alice
```

System-generated actions may not have a human actor.

Example:

```
action = AI_CLASSIFIED
user = null
```

---

### FR-022 — Track Human Overrides

The system shall record when a human changes an AI decision.

Examples:

* changing predicted priority
* changing predicted category
* editing an AI-generated response
* rejecting an AI suggestion

The original AI output should remain available for comparison.

---

## 6.7 AI Evaluation

### FR-023 — Classification Evaluation

The system should support evaluating ML classification performance.

Metrics may include:

* precision
* recall
* F1 score
* accuracy

---

### FR-024 — Override Rate

The system should track how often humans override AI predictions.

Example:

```
100 AI predictions
20 changed by agents

Override rate = 20%
```

---

### FR-025 — Response Editing Evaluation

The system should support measuring how often AI-generated responses are edited before approval.

---

### FR-026 — Model Version Tracking

Predictions shall identify which model version produced them.

This allows comparisons between models over time.

---

# 7. Non-Functional Requirements

Non-functional requirements describe **how the system should behave**, rather than individual features.

---

### NFR-001 — Security

Protected functionality shall require authentication.

Passwords must never be stored as plain text.

---

### NFR-002 — Authorization

The system shall restrict actions according to user permissions and roles.

---

### NFR-003 — Auditability

Important AI and human actions should be traceable.

The system should make it possible to answer:

```
What happened?
When did it happen?
Who performed the action?
What did the AI predict?
Did a human override it?
Who approved the final response?
```

---

### NFR-004 — Testability

Core application behavior shall be covered by automated tests.

Testing should include:

* authentication
* authorization
* ticket creation
* ticket access
* ticket assignment
* AI workflow
* approval workflow
* audit logging

---

### NFR-005 — API Documentation

The REST API shall be documented using an OpenAPI-compatible specification.

Swagger or similar tooling may be used to inspect:

* available endpoints
* request formats
* response formats
* authentication requirements

---

### NFR-006 — Maintainability

The application should maintain clear separation of concerns between:

* API handling
* business logic
* database access
* authentication
* AI/ML logic
* routing
* audit logging

This should make the system easier to understand, test, modify, and explain.

---

### NFR-007 — Containerization

The application shall be containerized using Docker.

This should provide a consistent environment across development and deployment.

---

### NFR-008 — Continuous Integration

The project shall eventually use automated Continuous Integration through GitHub Actions.

Typical flow:

```
Developer pushes code
        |
        v
   GitHub Actions
        |
        +--> install dependencies
        |
        +--> run automated tests
        |
        +--> run quality checks
        |
        +--> report pass/failure
```

---

### NFR-009 — Observability

The deployed application should expose useful operational metrics.

Later phases may monitor:

* request counts
* response times
* error rates
* application health
* CPU usage
* memory usage

Prometheus and Grafana are planned for monitoring and visualization.

---

### NFR-010 — Performance

The system should remain responsive under expected test workloads.

Load testing will later be performed using a tool such as:

* k6
* Locust

Example:

```
Simulate many users creating and viewing tickets
→ measure response times
→ find slow endpoints
→ identify failure points
```

---

### NFR-011 — Reliability

Failure of an AI component shall not make the core ticket system unusable.

Example:

```
Ticket created
    |
    v
AI classification fails
    |
    v
Ticket remains stored
    |
    v
Human agent can still handle it
```

The core support workflow must be able to continue when AI services fail.

---

## 8. Data Requirements

The initial main entities are:

* User
* Ticket
* Assignment
* AI Prediction
* Suggested Response
* Audit Log

Their fields and database relationships are documented separately in:

`docs/erd.md`

This separation is intentional:

* `srs.md` defines what information and behavior the system needs.
* `erd.md` defines how persistent data is structured.

---

## 9. Human-in-the-Loop Requirement

Human oversight is a core system requirement.

The system follows:

```
AI proposes
     |
     v
Human reviews
     |
     v
Human decides
     |
     v
System records decision
```

Example:

```
Ticket 101
     |
     v
AI predicts HIGH priority
     |
     v
Agent reviews prediction
   /             \
  /               \
Accept             Override
 HIGH              MEDIUM
  |                  |
  +--------+---------+
           |
           v
   Decision recorded
```

The same principle applies to AI-generated customer responses.

---

## 10. Assumptions

The initial system assumes:

* users have authenticated accounts
* customers submit text-based support tickets
* support agents handle tickets using the platform
* AI services may sometimes fail
* AI predictions may sometimes be incorrect
* humans remain responsible for customer-facing communication
* routing may initially be implemented with simple rules
* one person may have one primary role in the initial implementation
* the project is designed for learning and portfolio demonstration
* the project is not initially intended for enterprise-scale production usage

---

## 11. Out of Scope

The initial project will not attempt to reproduce every feature of commercial customer-support platforms.

The following are initially out of scope:

* fully autonomous ticket resolution
* sending AI-generated replies without human approval
* telephone call-center functionality
* voice-support systems
* advanced enterprise billing
* advanced enterprise SLA management
* full Zendesk/Freshdesk/Intercom feature parity
* production-grade Kubernetes infrastructure
* multi-region cloud architecture
* extreme-scale distributed infrastructure

These features may be discussed later but are not required for the planned portfolio system.

---

## 12. Failure and Edge Cases

### 12.1 AI Service Unavailable

If an AI service is unavailable:

```
Ticket received
    |
    v
Ticket stored
    |
    v
AI service fails
    |
    v
Ticket remains available
    |
    v
Human handles ticket
```

The ticket should not become unusable because an AI component failed.

---

### 12.2 Low-Confidence Prediction

An ML prediction may have low confidence.

The system should preserve the confidence score rather than presenting the prediction as certain.

Example:

```
category = BILLING
confidence = 0.52
```

This can later help agents and evaluation systems interpret the prediction.

---

### 12.3 Unassigned Ticket

A ticket may temporarily have no assigned support agent.

This is valid while routing or manual assignment is pending.

---

### 12.4 Response Waiting for Approval

An AI-generated response may exist without approval.

It must not be considered final customer-facing communication until a human approves it.

---

### 12.5 Human Override

A human may disagree with an AI prediction.

Example:

```
AI priority = HIGH

        ↓

Agent priority = MEDIUM
```

Both the original AI prediction and the human decision should remain traceable.

---

### 12.6 Ticket Reassignment

A ticket may move between agents.

Example:

```
Ticket 101
    |
    +--> Alice
    |
    +--> Bob
```

Previous assignments should remain stored instead of being overwritten.

---

## 13. Basic Use Cases

### UC-001 — Customer Creates Ticket

**Actor:** Customer

Flow:

```
Customer authenticates
    |
    v
Customer creates ticket
    |
    v
System validates request
    |
    v
Ticket stored
    |
    v
Status = NEW
```

---

### UC-002 — System Classifies Ticket

**Actor:** ML component

Flow:

```
New ticket
    |
    v
Ticket text analyzed
    |
    v
Category predicted
    |
    v
Priority predicted
    |
    v
Prediction metadata stored
```

---

### UC-003 — Ticket Is Assigned

**Actor:** Routing component or authorized user

Flow:

```
Ticket classified
    |
    v
Routing rules evaluated
    |
    v
Agent selected
    |
    v
Assignment created
    |
    v
Ticket becomes ASSIGNED
```

---

### UC-004 — Agent Handles Ticket

**Actor:** Support Agent

Flow:

```
Agent opens assigned ticket
    |
    v
Reviews ticket
    |
    v
Reviews AI predictions
    |
    v
Status becomes IN_PROGRESS
    |
    v
Agent works on issue
```

---

### UC-005 — AI Generates Suggested Response

**Actors:** Support Agent and LLM component

Flow:

```
Agent requests suggestion
    |
    v
Ticket context provided to LLM
    |
    v
LLM generates draft
    |
    v
Draft stored
    |
    v
Human review required
```

---

### UC-006 — Agent Approves Response

**Actor:** Support Agent

Flow:

```
Agent reviews AI draft
    |
    +--> edits if necessary
    |
    v
Agent approves response
    |
    v
Approval information stored
    |
    v
Audit event recorded
```

---

### UC-007 — Agent Overrides AI Prediction

**Actor:** Support Agent

Flow:

```
AI predicts HIGH
    |
    v
Agent reviews ticket
    |
    v
Agent decides MEDIUM
    |
    v
Final priority updated
    |
    v
Override logged
    |
    v
Original AI prediction preserved
```

---

## 14. Initial Acceptance Criteria

The initial system can be considered functionally complete when it demonstrates this end-to-end workflow:

```
1. Customer authenticates
2. Customer creates a ticket
3. Ticket is stored in PostgreSQL
4. Category is predicted
5. Priority is predicted
6. Prediction information is stored
7. Ticket is routed or assigned
8. Agent views the ticket
9. Agent can review AI predictions
10. LLM generates a suggested response
11. Agent reviews or edits the response
12. Agent approves the response
13. Important actions are logged
14. Human overrides remain traceable
15. AI performance can be evaluated
```

Meeting these criteria does **not** mean the system is production-grade.

It means the planned portfolio workflow has been implemented and demonstrated.

---

## 15. Related Documentation

The project documentation is organized as:

```
docs/
├── srs.md
├── architecture.md
├── erd.md
└── adr/
```

Purpose of each document:

### `srs.md`

Defines:

> What must the system do?

### `architecture.md`

Defines:

> How are the major technical components organized?

### `erd.md`

Defines:

> What persistent data exists and how is it related?

### `adr/`

Defines:

> Why did we make important technical decisions?

Examples of future ADRs:

* Why Django?
* Why PostgreSQL?
* Why REST?
* Why keep human approval?
* Why use assignment history instead of only storing the current agent?

---

## 16. Future Changes

This SRS is an initial design document and is expected to evolve.

Requirements may change when:

* implementation reveals missing behavior
* security concerns are discovered
* database design is refined
* tests reveal ambiguous requirements
* AI evaluation needs additional information
* architecture decisions change
* new edge cases are discovered

Changes should be deliberate and documented.

The implementation should not silently drift away from this specification.

---

## 17. Current Phase

This document belongs to **Phase 0 — Planning and Architecture**.

At this point:

* requirements are being defined
* architecture is being designed
* the ERD is being created
* major technical decisions will be documented using ADRs

Application implementation has not yet started.

The next phases will translate these requirements into:

```
Requirements
    |
    v
Architecture
    |
    v
Database design
    |
    v
Django models
    |
    v
REST APIs
    |
    v
Authentication / RBAC
    |
    v
Tests
    |
    v
AI / ML components
    |
    v
Deployment and operations
```
