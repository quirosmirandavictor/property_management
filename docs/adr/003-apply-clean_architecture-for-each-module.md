# ADR-003: Apply Clean architecture for each module

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

### Option A: Django MVT

**Pros**

- **Rapid development:** Django's built-in conventions, ORM, admin interface, and authentication accelerate feature delivery.
- **Mature ecosystem:** Extensive documentation, community support, and reusable packages.
- **Lower initial complexity:** A well-defined project structure reduces architectural decisions for small or medium-sized applications.

**Cons**

- **Framework coupling:** Business logic tends to become dependent on Django models, views, and framework-specific components.
- **Harder to enforce module boundaries:** MVT does not naturally promote explicit separation between domain and infrastructure concerns.
- **Reduced long-term maintainability:** As the system grows, business rules can spread across models, views, and serializers, increasing technical debt.

### Option B: Traditional Layered Architecture (N-Tier)

**Pros**

- **Simple and familiar:** A widely adopted architecture that is easy for most developers to understand.
- **Clear technical separation:** Presentation, business, and data access responsibilities are organized into distinct layers.
- **Suitable for CRUD applications:** Works well for applications with relatively simple business rules.

**Cons**

- **Business logic depends on infrastructure:** Domain services often become tightly coupled to persistence and framework implementations.
- **Limited flexibility:** Replacing databases or external technologies typically requires changes across multiple layers.
- **Weaker domain isolation:** Layer boundaries alone do not guarantee independence of business rules or low coupling between modules.

### Option C: Clean Architecture (Selected)

**Pros**

- **Framework independence:** Business rules remain isolated from frameworks, databases, and external technologies.
- **High maintainability and testability:** Domain and application layers can be tested without infrastructure dependencies.
- **Supports modular evolution:** Well-defined boundaries allow modules to evolve independently and simplify future extraction into microservices.

**Cons**

- Higher initial complexity due to additional layers and abstractions.
- Requires disciplined enforcement of architectural boundaries across the development team.
- More boilerplate than framework-centric approaches, especially for smaller features.

## Consequences

### Positive

- **Framework independence:** Business rules remain isolated from Framework, the database, and external technologies, reducing vendor lock-in.
- **Improved maintainability:** Clear separation of responsibilities makes the codebase easier to understand, modify, and extend.
- **Higher testability:** Domain and application logic can be unit tested without relying on infrastructure components.
- **Supports modular evolution:** Explicit module boundaries simplify future extraction into independent services if required.

### Negative / Trade-offs

- **Higher initial complexity:** Additional layers, interfaces, and dependency inversion introduce more architectural overhead.
- **More boilerplate code:** Simple features may require additional abstractions compared to framework-centric approaches.
- **Requires architectural discipline:** The team must consistently enforce dependency rules and module boundaries to prevent architectural erosion.

### Items to Monitor

- **Boundary violations:** Ensure dependencies always point inward and modules do not access each other's internal implementations.
- **Architecture consistency:** Verify that new features follow the established Clean Architecture structure instead of introducing shortcuts.
- **Testing coverage:** Monitor the proportion of unit tests focused on the domain and application layers to ensure business logic remains independent.

## References

- ADR-001: Adopt a modular monolith architecture
- Robert C. Martin — *Clean Architecture: A Craftsman's Guide to Software Structure and Design*
- Martin Fowler — *Patterns of Enterprise Application Architecture*