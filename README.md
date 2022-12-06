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

## Parts of the service

* [Public Access UI](https://github.com/nationalarchives/ds-caselaw-public-ui)
* [Editorial UI](https://github.com/nationalarchives/ds-caselaw-editor-ui)
* [Ingester](https://github.com/nationalarchives/ds-caselaw-ingester)
* [PDF conversion](https://github.com/nationalarchives/ds-caselaw-pdf-conversion)
* [Privileged API](https://github.com/nationalarchives/ds-caselaw-privileged-api)

Want an overview of all our repositories? Check the [repository dashboard](/repo-dashboard.md).

### Configuration

For historical reasons, some parts of the service are contained in this repository.

* [Marklogic database configuration](https://github.com/nationalarchives/ds-find-caselaw-docs/tree/main/marklogic)
* [OpenAPI specification](https://github.com/nationalarchives/ds-find-caselaw-docs/tree/main/doc/openapi)

### Shared support libraries

* [API client](https://github.com/nationalarchives/ds-caselaw-custom-api-client)
* [Utility library](https://github.com/nationalarchives/ds-caselaw-utils)

### Content

* [Custom PDFs](https://github.com/nationalarchives/ds-caselaw-custom-pdfs)

### Prototypes

Design-phase prototype code.

* [Prototypes](https://github.com/nationalarchives/ds-caselaw-prototypes)
* [Frontend Prototypes](https://github.com/nationalarchives/ds-caselaw-frontend)
* [Marklogic Prototype](https://github.com/mangiafico/tna-judgments-website)

## Related services

Services provide data to, or take data from, this system.

* [Transformation Engine](https://github.com/nationalarchives/da-transform-dev-documentation/blob/develop/editorial-system-integration/README.md)
* [Enrichment Service](https://github.com/nationalarchives/ds-caselaw-data-enrichment-service)

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
