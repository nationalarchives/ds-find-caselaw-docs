# Case Law Public Access Service

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Table of Contents

- [Background](#background)
- [Services](#services)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Background

This is the central repository for the Case Law Public Access service. It includes architectural decisions, designs, and links to individual code repositories for the various component [microservices](doc/adr/0002-use-a-microservice-architecture.md).

## Services

* [Public Access UI](https://github.com/nationalarchives/ds-caselaw-public-ui/)

### Related services

* [Transformation Engine](https://github.com/nationalarchives/da-transform-dev-documentation/blob/develop/editorial-system-integration/README.md)

### Prototypes

* [Frontend Prototypes](https://github.com/nationalarchives/ds-caselaw-frontend)
* [Marklogic Prototype](https://github.com/mangiafico/tna-judgments-website)

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
