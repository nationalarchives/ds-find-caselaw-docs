# Custom Caselaw Marklogic roles

`src/main/ml-config/security/roles` contains the Gradle configurations for the custom Caselaw roles.
All users added to Marklogic should use one or more of these roles. No users (aside from the admin users
`caselaw-prod-marklogic` and `caselaw-staging-marklogic`) should have `admin` privileges in Marklogic.

Helpful Marklogic links:
- [Execute privileges](https://docs.marklogic.com/guide/admin/exec_privs)
- [Pre-defined roles](https://docs.marklogic.com/guide/admin/pre_def_roles)

## caselaw-nobody

The base Caselaw role with no privileges.

## caselaw-reader

This role allows the user to view published documents via the `rest-reader` pre-defined role.

It inherits the `security` role to check the user's execute privileges.

It inherits `dls-*` roles in order to be able to read document properties.

It requires two execute privileges, `xdbc-eval` and `xdbc-invoke`. 
- `xdbc-eval` is required by Marklogic to call the `eval` endpoint, which is used for the XSLT transformation. 
- `xdbc-invoke` is required by Marklogic to call the `invoke` endpoint, which is used for search.

## caselaw-unpublished-reader

This role inherits everything from `caselaw-reader`, and also has a custom execute privilege `can-view-unpublished-documents`
which allows the user to read unpublished documents.

## caselaw-writer

This role allows the user to write documents. It inherits everything from `caselaw-reader` and `caselaw-unpublished-reader`
as well as allowing the user to write documents via the `rest-writer` pre-defined role.

## caselaw-priv-api-writer

This role inherits everything from `caselaw-writer` and  `caselaw-unpublished-reader` and is intended for users who
only need to access the privileged API.

## caselaw-admin

A role intended for admins on the Caselaw project who do not need full Marklogic `admin` access.