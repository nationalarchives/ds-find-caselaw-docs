# Document flow diagram

This charts the flow a document takes, from submission to TDR by the clerk through to being viewable by members of the public. It does not include an exhaustive expansion of the journey through processes such as TDR or Enrichment.

```mermaid
stateDiagram
    direction LR

    classDef nonfcl fill:#fafafa,color:#888,stroke:#888;
    classDef lambda stroke-width:2,stroke:#77F;
    classDef application stroke-width:2,stroke:#7C7;

    % Submission flows

    class Clerk nonfcl
    class TDR nonfcl
    class TRE nonfcl
    class Parser lambda
    class Ingester lambda

    [*] --> Clerk
    Clerk --> TDR
    TDR --> TRE
    TRE --> Parser
    Parser --> TRE
    TRE --> Ingester
    Ingester --> MarkLogic
    TRE --> S3
    S3 --> Ingester

    % Approval workflows

    class EUI application

    MarkLogic --> EUI
    EUI --> MarkLogic
    EUI --> Clerk

    % Public workflows

    class PUI application

    MarkLogic --> PUI
    PUI --> [*]
    S3 --> [*]

    % Enrichment flows

    class Enrichment lambda
    class PAPI application

    PAPI : Privileged API
    MarkLogic --> PAPI
    PAPI --> Enrichment
    Enrichment --> PAPI
    PAPI --> MarkLogic
    S3 --> Enrichment
    Enrichment --> S3

    % Re-processing flows

    EUI --> TRE
    EUI --> Enrichment
```
