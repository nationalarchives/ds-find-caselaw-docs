# 2. Use a microservice architecture

Date: 2022-01-31

## Status

Accepted

## Context

The Court Judgments service is made up of a number of components, some of which already exist in research form, and some of which are to be created as part of the development process towards a live service. These use a variety of technologies and platforms. It also interacts with some existing services within TNA.

- Email lists: judgments are received from courts via email
- Transfer Digital Records: TNA tool for uploading documents to the archive, will be used by courts in future
- Document parser: built in C#, responsible for converting .DOCX files into LegalDocML format
- Validation engine: schematron validator to ensure correct XML
- Judgment database: currently using Marklogic, an XML-oriented document database
- Administration interface: a new application to review, approve, and edit judgments
- Public access site: a new application to display judgments on the public Internet

There are also other services which will update judgments, such as the Enrichment service.

## Decision

We will build the Court Judgments service using a microservice architecture.

Microservice architecture[^microservices] is an approach to building applications as a suite of small interacting components, with defined interfaces between them, where each can be developed and deployed independently. This pattern fits well with the range of existing services we intend to integrate and allows different languages and technologies to be used as most appropriate.

We will define lightweight REST interfaces[^rest] between components, or use existing API definitions where available. These interfaces will be documented separately.

Starting from scratch with a microservice architecture is often not the right approach[^monolith-first]. However, in this case we already have a suite of components that need to interact, so taking a monolithic approach first would be more complex.

## Consequences

Microservice architectures can become overly complex. We should be careful only to split out services where really appropriate, and keep interfaces well-defined and well-documented. Data should be held centrally to avoid synchronisation problems across services.

[^microservices]: [Microservices Guide](https://www.martinfowler.com/microservices/), Martin Fowler
[^rest]: [REST APIs](https://en.wikipedia.org/wiki/Representational_state_transfer)
[^monolith-first]: [Monolith First](https://www.martinfowler.com/bliki/MonolithFirst.html), Martin Fowler
