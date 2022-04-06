# Marklogic Database Configuration

This folder specifies the configuration of the Marklogic database used by the
Case Law public access system. It uses the [ml-gradle](https://github.com/marklogic/ml-gradle)
to manage and maintain a versioned configuration.

For full details of what can be set in the files here, see the
[ml-gradle documentation](https://github.com/marklogic-community/ml-gradle/wiki).
The file layout is explaines in the [project layout documentation](https://github.com/marklogic-community/ml-gradle/wiki/Project-layout).

## Setup

1. Install `gradle`. On MacOS, you can use `brew install gradle`.

2. Copy `gradle-example.properties` to `gradle-local.properties` and set the credentials
and hostname for your Marklogic server.

A `docker-compose.yml` file for running Marklogic locally is included. Run `docker-compose up` to start it.

## Deployment

To deploy the configuration, run `gradle mlDeploy`. Deployment is idempotent, and will automatically
configure databases, roles, triggers and modules.

## Document processing

Two gradle tasks are available for bulk management of documents in a database using
[CoRB](https://github.com/marklogic-community/corb2). In production these should not be
necessary to use, but are provided in order to automate some development tasks and provide
examples for future data migrations.

* `gradle manageAllDocuments`: Enables version management for all documents
* `gradle publishAllDocuments`: Sets the `published` flag for all documents
