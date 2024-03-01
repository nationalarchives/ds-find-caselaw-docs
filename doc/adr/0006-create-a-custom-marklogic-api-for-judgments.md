# 6. Create a custom Marklogic API for Judgments

Date: 2022-02-21

## Status

Accepted

## Context

Marklogic has a basic REST API for documents, but many advanced features are not exposed in that way, and instead
require the use of XQuery APIs.

We need to use XQUery APIs in order to use the Library Services feature agreed in ADR 0005.

The REST API has an endpoint which allows [execution of arbitrary XQuery](https://docs.marklogic.com/guide/rest-dev/extensions#id_67576),
but allowing all clients to use that seems dangerous.

Marklogic allows the creation of applications which run within it, and which can use the XQuery APIs. The default
REST API is one of these applications.

The default REST API can be [extended](https://docs.marklogic.com/guide/rest-dev/extensions) with custom code. Extensions
can add their own REST endpoints, using GET, PUT, POST and/or DELETE verbs.

## Decision

We will create our own custom endpoints by extending the REST API.

These endpoints will provide a domain-specific wrapper API around the Marklogic Library Services feature. They will support check in/out,
updating, reading, and editing of document metadata.

We will design that API to use the URI scheme defined in ADR 0004 as closely as possible.

All clients will communicate with Marklogic via the extended REST API, in line with ADR 0003.

The API will be documented with an [OpenAPI](https://swagger.io/specification/) specification, which will define available endpoints, authentication schemes and so on. The canonical
version of that specification can be found [in this repository](../openapi/), and will be iterated based on client needs.

We will continue to use the default REST API for read-only actions and search, at least for the short term. The new API endpoints will
only be used for write operations. The OpenAPI specification will include the standard endpoints as well, for completeness.

Ideally, external API users of the service will be able to use our domain-specific API directly.

## Consequences

The standard REST API may not be suitable for exposure to external API users. If not, the extension code may be turned into a complete
custom API application rather than an extension, and the standard REST API disabled.

Marklogic extensions are written in Javascript; this will add another language to the project.
