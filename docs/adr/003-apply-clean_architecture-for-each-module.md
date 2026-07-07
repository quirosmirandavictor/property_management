# ADR-004: Apply Clean architecture for each module

## Status

Accepted <!-- Proposed | Accepted | Rejected | Deprecated | Superseded -->

## Date

2026-06-26

## Context

The legacy project relied on Django's built-in MVT architecture for the backend. Over time, the framework became tightly coupled to the application's business logic, making domain rules dependent on infrastructure and framework-specific components.

This approach led to poor separation of concerns, business logic leaking into inappropriate layers, and a codebase that became increasingly difficult to maintain, test, and evolve.

The new system will remain a modular monolith, but each module must be designed with clear architectural boundaries and low coupling. This will allow modules to evolve independently and provide a straightforward path to extracting them into microservices if future scalability or business requirements demand it.

## Decision

We will use clean architecture, each module of the application will follow the principles of Clean Architecture. Business rules will reside in the domain and application layers, independent of frameworks, databases, and external technologies.

Dependencies will always point inward, following the Dependency Inversion Principle. Frameworks, persistence mechanisms, and external services will be treated as implementation details through adapters and interfaces.

The system will be developed as a modular monolith with explicit boundaries between modules. Each module should expose only well-defined interfaces and avoid direct dependencies on the internal implementation of other modules.

## Alternatives Considered


## Consequences

### Positive


### Negative / Trade-offs

### Items to Monitor

## References