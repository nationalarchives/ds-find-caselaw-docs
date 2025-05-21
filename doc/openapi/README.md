# OpenAPI Specifications

> [!WARNING]
> You need to [apply for a licence to do computational analysis](https://caselaw.nationalarchives.gov.uk/computational-licence-form) of Find Case Law records. Other use is licenced under the [Open Justice Licence](https://caselaw.nationalarchives.gov.uk/about-this-service#section-licences).

We document our APIs using OpenAPI specifications, so that they can easily interface with other tools.

## Documentation

Our specifications are automatically compiled into human-readable documentation using the [Redocly CLI](https://redocly.com/docs/redoc/deployment/cli) and published:

- https://nationalarchives.github.io/ds-find-caselaw-docs/public
- https://nationalarchives.github.io/ds-find-caselaw-docs/privileged

### Generating documentation locally

If you want to generate the documentation locally, first install Redocly CLI:

```shell
npm i -g @redocly/cli@latest
```

Then, run Redocly against the OpenAPI specs using `npx`:

```shell
npx @redocly/cli build-docs doc/openapi/public_api.yml
```

## Linting

We lint our documentation using [Optic](https://github.com/opticdev/optic) to make sure it's consistent and complete.

Optic is run as part of our test suite using pre-commit, but can also be installed and run manually:

```shell
npm install -g @useoptic/optic
```

```shell
optic diff doc/openapi/public_api.yml
```
