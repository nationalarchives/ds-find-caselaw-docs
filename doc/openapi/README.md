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

## Validation and breaking changes

Structural OpenAPI validity is checked with [openapi-spec-validator](https://github.com/python-openapi/openapi-spec-validator) via pre-commit.

Pull requests that touch the public API are also checked with [oasdiff](https://github.com/oasdiff/oasdiff) via [oasdiff-action](https://github.com/oasdiff/oasdiff-action):

- breaking changes fail the check
- a changelog of consumer-facing changes is posted as a PR comment

To run the same breaking-change check locally (against `main`):

```shell
oasdiff breaking origin/main:doc/openapi/public_api.yml doc/openapi/public_api.yml
```
