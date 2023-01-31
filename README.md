# Case Law Public Access Service

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Table of Contents

- [Background](#background)
- [Services](#services)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Background

This is the central repository for the [Case Law Public Access service](https://caselaw.nationalarchives.gov.uk/). It includes [architectural decisions](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/doc/adr),[technical designs](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/doc/arch), and links to individual code repositories for the various component [microservices](doc/adr/0002-use-a-microservice-architecture.md).

## Services

* [Public Access UI](https://github.com/nationalarchives/ds-caselaw-public-ui/)
* [Editorial UI](https://github.com/nationalarchives/ds-caselaw-editor-ui/)
* [Ingester](https://github.com/nationalarchives/ds-caselaw-ingester)
* [PDF conversion](https://github.com/nationalarchives/ds-caselaw-pdf-conversion)
* [Marklogic database configuration](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/marklogic)
* [OpenAPI spec](https://github.com/nationalarchives/ds-caselaw-public-access-service/tree/main/doc/openapi)

### Shared support libraries

* [API client](https://github.com/nationalarchives/ds-caselaw-custom-api-client)
* [Utility library](https://github.com/nationalarchives/ds-caselaw-utils)

### Related services

Services provide data to, or take data from, this system.

* [Transformation Engine](https://github.com/nationalarchives/da-transform-dev-documentation/blob/develop/editorial-system-integration/README.md)
* [Enrichment Service](https://github.com/nationalarchives/ds-caselaw-data-enrichment-service)

### Prototypes

Design-phase prototype code.

* [Frontend Prototypes](https://github.com/nationalarchives/ds-caselaw-frontend)
* [Marklogic Prototype](https://github.com/mangiafico/tna-judgments-website)

## Architecture

<details>
  <summary>System Landscape Diagram</summary>

  ```mermaid
        C4Context
        title System landscape

        System_Ext(tdr, "Transfer Digital Records")

        Person_Ext(apiUser, "API User")
        Person_Ext(joepublic, "Public User")
        Person(editor, "TNA Editorial Team")
        

        
        System_Ext(transformationEngine, "Transformation Engine")
        System_Ext(enrichment, "Enrichment Engine")

        System_Boundary(access, "Case Law Access") {
            System(ingester, "Ingester")
            System(api, "REST API", $tags="Marklogic Application")
            System(publicUI, "Public UI")
            System(editorUI, "Editor UI")
            
            
            SystemDb(markLogic, "LegalDocML document store", "MarkLogic")
        }

        BiRel(api, markLogic, "queries", "XQuery")

        Rel(tdr, transformationEngine, "sends uploaded documents")
        Rel(transformationEngine, ingester, "sends parsed documents", "S3/SNS")
        Rel(ingester, api, "stores documents", "HTTPS")
        BiRel(enrichment, api, "reads/writes", "HTTPS")
        BiRel(editorUI, api, "reads/writes", "HTTPS")
        Rel(publicUI, api, "reads", "HTTPS")
        Rel_R(apiUser, api, "reads", "HTTPS")
        Rel(joepublic, publicUI, "uses", "HTTPS")
        Rel(editor, editorUI, "uses", "HTTPS")
  ```
</details>

<details>
  <summary>Container Diagram</summary>

  ![Container Diagram](doc/arch/images/Container%20Diagram.png)
</details>

<details>
  <summary>Deployment Diagram</summary>

  ![Deployment Diagram](doc/arch/images/Deployment%20Diagram.png)
</details>

## Contributing

### Behaviour and safety

We want everybody to be safe when interacting with this project. So,
anybody raising an issue or opening a pull request is expected to
follow the Contributor Covenant
[Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

### What to expect

This project is not actively seeking external contributions. If you raise an
issue or open a pull request, we will do our best to respond to it, but we
can’t guarantee that we will fix or merge anything.

If you’re thinking about putting a lot of work into a pull request, and would
like to get a better idea of whether we’d consider merging it, we advise that
you first open a GitHub issue so that we can talk about it.

## License

[MIT](LICENSE.md) © Crown Copyright (The National Archives)
