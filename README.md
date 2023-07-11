# The National Archives: Find Case Law

This repository is part of the [Find Case Law](https://caselaw.nationalarchives.gov.uk/) project at [The National Archives](https://www.nationalarchives.gov.uk/).

# Project Documentation

## Table of Contents

- [Background](#background)
- [Parts of the service](#parts-of-the-service)
- [Architecture](#architecture)

## Background

This is the central repository for the [Find Case Law service](https://caselaw.nationalarchives.gov.uk/). It includes [architectural decisions](https://github.com/nationalarchives/ds-find-caselaw-docs/tree/main/doc/adr), [technical designs](https://github.com/nationalarchives/ds-find-caselaw-docs/tree/main/doc/arch), and links to individual code repositories for the various component [microservices](doc/adr/0002-use-a-microservice-architecture.md).

If you are looking for documentation covering user research, design decisions or accessibility, take a look at the [Wiki](https://github.com/nationalarchives/ds-find-caselaw-docs/wiki).

## Repositories

<!-- Begin list of repositories -->
<!-- This section is automatically generated from scripts/build_repo_lists. You shouldn't edit it manually. -->

| Repository                                                                                                   | Description                                                  |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| [ds-find-caselaw-docs](https://github.com/nationalarchives/ds-find-caselaw-docs)                             | High-level documentation for the service.                    |
| [ds-caselaw-public-ui](https://github.com/nationalarchives/ds-caselaw-public-ui)                             | Public interface to the service.                             |
| [ds-caselaw-editor-ui](https://github.com/nationalarchives/ds-caselaw-editor-ui)                             | Editor interface to the service.                             |
| [ds-caselaw-marklogic](https://github.com/nationalarchives/ds-caselaw-marklogic)                             | MarkLogic database configuration.                            |
| [ds-caselaw-ingester](https://github.com/nationalarchives/ds-caselaw-ingester)                               | Ingests cases from the Transformation Engine into MarkLogic. |
| [ds-caselaw-pdf-conversion](https://github.com/nationalarchives/ds-caselaw-pdf-conversion)                   | Converts a judgement to PDF.                                 |
| [ds-caselaw-privileged-api](https://github.com/nationalarchives/ds-caselaw-privileged-api)                   | The API which annotating services talk to.                   |
| [ds-caselaw-custom-api-client](https://github.com/nationalarchives/ds-caselaw-custom-api-client)             | API client to interface with MarkLogic.                      |
| [ds-caselaw-utils](https://github.com/nationalarchives/ds-caselaw-utils)                                     | Common utilities across codebases.                           |
| [ds-caselaw-custom-pdfs](https://github.com/nationalarchives/ds-caselaw-custom-pdfs)                         | Custom PDFs to overwrite generated ones.                     |
| [ds-caselaw-data-enrichment-service](https://github.com/nationalarchives/ds-caselaw-data-enrichment-service) | Detect and tag references to legal documents.                |

<!-- End list of repositories -->

See the [repository dashboard](/repo-dashboard.md) for an overview of things like pull requests and release versions.

### Configurations

For historical reasons, some parts of the service are contained in this repository.

- [OpenAPI specification](https://github.com/nationalarchives/ds-find-caselaw-docs/tree/main/doc/openapi)

### Other repositories

#### Prototypes

Design-phase prototype code.

- [Prototypes](https://github.com/nationalarchives/ds-caselaw-prototypes)
- [Frontend Prototypes](https://github.com/nationalarchives/ds-caselaw-frontend)
- [Marklogic Prototype](https://github.com/mangiafico/tna-judgments-website)

#### Related services

Services provide data to, or take data from, this system.

- [Transformation Engine](https://github.com/nationalarchives/da-transform-dev-documentation/blob/develop/editorial-system-integration/README.md)
- [Enrichment Service](https://github.com/nationalarchives/ds-caselaw-data-enrichment-service)

## Architecture

<details>
  <summary>System Landscape Diagram</summary>

![System Landscape Diagram](doc/arch/images/System%20Landscape.png)

</details>

<details>
  <summary>Container Diagram</summary>

![Container Diagram](doc/arch/images/Container%20Diagram.png)

</details>

<details>
  <summary>Deployment Diagram</summary>

![Deployment Diagram](doc/arch/images/Deployment%20Diagram.png)

</details>

## Manual data changes

Sometimes we need to [delete or restore judgments](doc/changing-judgments/changing-judgments.md).
