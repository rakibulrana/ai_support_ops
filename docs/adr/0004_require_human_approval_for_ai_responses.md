# ADR 0004: Require Human Approval for AI Responses

## Status

Accepted

## Context

The system will use an LLM to generate suggested customer responses.

AI-generated text can be incorrect, incomplete, or inappropriate.

Customer-facing communication should therefore remain under human control.

## Decision

Require a Support Agent to review and approve every AI-generated customer response before it is treated as final.

## Why

This provides:

- human oversight
- safer customer communication
- clear accountability
- better auditability
- useful data for measuring AI quality

## Alternatives Considered

- Automatically send AI-generated responses
- Require approval only for low-confidence responses

Automatic sending would create unnecessary risk for this project.

Confidence-based approval could be explored later, but it adds complexity and still depends on reliable confidence estimation.

## Consequences

Positive:

- humans remain responsible for final communication
- AI mistakes can be caught before reaching customers
- edits and overrides can be measured
- approval actions can be audited

Trade-offs:

- responses are not fully automated
- support agents still need to review drafts
- approval adds an extra workflow step