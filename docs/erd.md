# Entity Relationship Diagram

## Main Entities

- User                      = customer, agent, or admin.
- Ticket                    = the support request.
- Assignment                = which agent handles a ticket.
- AI Prediction             = predicted category/priority.
- Suggested Response        = AI-generated draft.
- Audit Log                 = record of important actions.

## Relationships

- One User can create many Tickets.
- One Ticket belongs to one Customer.
- One Ticket can have many Assignment.
- One Support Agent can have many Assignments over time.
- One Ticket can have many AI Predictions.
- One Ticket can have many Suggested Responses.
- One Ticket can have many Audit Logs.



## Entity Fields

### Ticket

- id                            = unique ticket number
- title                         = short issue summary
- description                   = full customer problem
- status                        = NEW, ASSIGNED, RESOLVED, etc.
- priority                      = low/medium/high
- category                      = billing, technical, account, etc.
- created_by                    = which customer created it
- created_at                    
- updated_at            

### User

- id
- name
- email
- password                      = stored securely as a hash, never plain text
- role                          = CUSTOMER, AGENT, or ADMIN
- created_at                    = when the account was created


### Assignment

- id
- ticket_id
- agent_id
- assigned_at
- unassigned_at                 = when it ended




### AI Prediction

- id                               
- ticket_id                         = which ticket was analyzed
- predicted_category                = e.g. billing, technical
- predicted_priority
- model_version                     = which ML model made the prediction
- confidence_score                  = how confident the model was
- created_at                        = when prediction happened


### Suggested Response

- id
- ticket_id
- generated_text                    = original AI draft
- edited_text                       = agent's edited version, if changed
- approved_by
- approved_at
- created_at



### Audit Log

- id
- ticket_id
- user_id                           = who performed the action, if a human did it  (optional)
- action                            = e.g. TICKET_CREATED, AI_CLASSIFIED, RESPONSE_APPROVED
- details                           = extra information about what changed
- created_at




## ERD diagram: 


User
  |
  | creates
  v
Ticket
  |
  +----< Assignment >---- User(agent)
  |
  +----< AI Prediction
  |
  +----< Suggested Response
  |
  +----< Audit Log


  USER
----------------
PK id
   name
   email
   role

      1
      |
      | creates
      |
      many

TICKET
----------------
PK id
FK created_by
   title
   description
   status
   priority
   category

      1
      |
      | has
      |
      many

ASSIGNMENT
----------------
PK id
FK ticket_id
FK agent_id
   assigned_at
   unassigned_at



