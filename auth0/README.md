# Auth0 Tenant Configuration

This folder specifies the configuration of the Auth0 tenant used by the
Case Law Editorial UI. It uses the [Auth0 CLI Deployment tool](https://github.com/auth0/auth0-deploy-cli)
to manage and maintain a versioned configuration.

For full details of what can be set in the files here, see the
[example](https://github.com/auth0/auth0-deploy-cli/tree/master/examples/directory).

## Setup

Copy `config.example.json` to `config.json` and set the Client ID and
Secret from the `auth0-deploy-cli-extension` application in Auth0.

Run `make setup` to install the CLI tool.

## Deployment

To deploy the configuration, run `make deploy`.

Note that deletions are disabled.

## Export

To save the remote Auth0 configuration as JSON files in this directory,
run `make export`.
