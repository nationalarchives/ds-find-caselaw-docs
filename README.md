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
      title System Context diagram for Internet Banking System
      Enterprise_Boundary(b0, "BankBoundary0") {
        Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
        Person(customerB, "Banking Customer B")
        Person_Ext(customerC, "Banking Customer C", "desc")

        Person(customerD, "Banking Customer D", "A customer of the bank, <br/> with personal bank accounts.")

        System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")

        Enterprise_Boundary(b1, "BankBoundary") {

          SystemDb_Ext(SystemE, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

          System_Boundary(b2, "BankBoundary2") {
            System(SystemA, "Banking System A")
            System(SystemB, "Banking System B", "A system of the bank, with personal bank accounts. next line.")
          }

          System_Ext(SystemC, "E-mail system", "The internal Microsoft Exchange e-mail system.")
          SystemDb(SystemD, "Banking System D Database", "A system of the bank, with personal bank accounts.")

          Boundary(b3, "BankBoundary3", "boundary") {
            SystemQueue(SystemF, "Banking System F Queue", "A system of the bank.")
            SystemQueue_Ext(SystemG, "Banking System G Queue", "A system of the bank, with personal bank accounts.")
          }
        }
      }

      BiRel(customerA, SystemAA, "Uses")
      BiRel(SystemAA, SystemE, "Uses")
      Rel(SystemAA, SystemC, "Sends e-mails", "SMTP")
      Rel(SystemC, customerA, "Sends e-mails to")

      UpdateElementStyle(customerA, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateRelStyle(customerA, SystemAA, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(SystemAA, SystemE, $textColor="blue", $lineColor="blue", $offsetY="-10")
      UpdateRelStyle(SystemAA, SystemC, $textColor="blue", $lineColor="blue", $offsetY="-40", $offsetX="-50")
      UpdateRelStyle(SystemC, customerA, $textColor="red", $lineColor="red", $offsetX="-50", $offsetY="20")

      UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
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
