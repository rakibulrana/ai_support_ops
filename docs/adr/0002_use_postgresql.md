# ADR 0002: Use PostgreSQL

## Status

Accepted

## Context

The system needs a relational database for storing:

- users
- tickets
- assignments
- AI predictions
- suggested responses
- audit logs

The data has clear relationships and needs reliable constraints.

## Decision

Use PostgreSQL as the primary application database.

## Why

PostgreSQL provides:

- strong relational data support
- foreign keys and constraints
- transactions
- indexing
- good Django integration
- mature production usage

## Alternatives Considered

- SQLite
- MySQL
- MongoDB

SQLite is useful for small/local applications, but PostgreSQL is more appropriate for learning realistic backend development.

MongoDB is flexible, but our data is strongly relational, so a relational database is a better fit.

## Consequences

Positive:

- strong data integrity
- good support for relational queries
- realistic database experience
- strong Django compatibility

Trade-offs:

- requires a separate database service
- slightly more setup than SQLite
- database configuration must be managed correctly