# 4. Adopt a standardised URL scheme

Date: 2022-02-21

## Status

Accepted

## Context

We want a consistent URI/URL structure for case law that meets a number of requirements:

- We need a way to uniquely identify documents.
- We need a scheme that supports all initial data and features and is easily extensible for data and features we are likely to want to add in the near future.
- We want to support a RESTful API for data access with appropriate use of HTTP response codes following best practice principles for publishing linked data online.
- We want URIs to be as “hackable” as possible.
- We want to use URIs that closely match the way people usually cite documents so make the website as accessible as possible.
- We want to use information that is contained in the documents, as far as possible, and invent as little of our own as we can.
- We are looking to adopt a scheme which can directly map to the European Case Law Identifiers (ECLI), where ECLIs will also use the neutral citation (where it exists).
- We are looking to adopt a scheme which is broadly consistent with www.legislation.gov.uk URIs (i.e. with /id/ and /data.{ext} for formats).

## Decision

We will use the URI scheme designed by Catherine Tabone et al to define URLs across all case law services. We may need to extend
it for edit actions, etc, but the scheme should be used as proposed to identify documents. The full specification of the URI
scheme is not included here for brevity; instead we will use a subset of example URLs from that document. For the full
specification, refer to the [original definition](https://nationalarchivesuk.sharepoint.com/:w:/r/sites/LS_project/Data%20Development/Judgments%20Data%20Conversion/URI%20Scheme/Judgments%20URI%20Scheme%2016-02-2022.docx?d=w59ef433f65804907b734ec2657b5316d&csf=1&web=1&e=Ghcz6d).

### Judgments

#### Expressions

Expression URIs are the HTML versions of a judgment; what most people will use and see in their browser.

- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/]{year}/{neutral-citation-number}
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/]{year}/{judgment-date}/num/{tna-ordinal-number} (if no neutral citation defined)

Examples:

- https://caselaw.nationalarchives.gov.uk/ewhc/ch/2021/3346
- https://caselaw.nationalarchives.gov.uk/ewfc/2015/8
- https://caselaw.nationalarchives.gov.uk/uksc/2021/43
- https://caselaw.nationalarchives.gov.uk/ewca/crim/2021/1786
- https://caselaw.nationalarchives.gov.uk/ewfc/2021/2021-11-03/num/2

#### Manifestations

Manifestation URIs include an explicit format, with the `data` path component and the format appended as an extension. The expression URL is equivalent to the `data.html` manifestation URL.

- https://caselaw.nationalarchives.gov.uk/ewhc/ch/2021/3346/data.html
- https://caselaw.nationalarchives.gov.uk/ewfc/2015/8/data.xml
- https://caselaw.nationalarchives.gov.uk/uksc/2021/43/data.xml
- https://caselaw.nationalarchives.gov.uk/ewca/crim/2021/1786/data.pdf
- https://caselaw.nationalarchives.gov.uk/ewfc/2021/2021-11-03/num/2/data.html

#### Works

Work URIs are the canonical identifier for a judgment. These would not normally be used by a browser, but if they are requested, they should send a 303 response pointing to the current expression URL.

- https://caselaw.nationalarchives.gov.uk/id/ewhc/ch/2021/3346
- https://caselaw.nationalarchives.gov.uk/id/ewfc/2015/8
- https://caselaw.nationalarchives.gov.uk/id/uksc/2021/43
- https://caselaw.nationalarchives.gov.uk/id/ewca/crim/2021/1786
- https://caselaw.nationalarchives.gov.uk/id/ewfc/2021/2021-11-03/num/2

### Lists

- https://caselaw.nationalarchives.gov.uk/{court}
- https://caselaw.nationalarchives.gov.uk/{court}?page=x
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}]
- https://caselaw.nationalarchives.gov.uk/{year}
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}]/{year}
- https://caselaw.nationalarchives.gov.uk/{judgment-date}
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/]/{judgment-date}
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/]{year}/{judgment-date}

#### Manifestations

All lists should be available in a variety of formats with the `data.html` being the default as before, e.g.

- https://caselaw.nationalarchives.gov.uk/{court}/data.ext
- https://caselaw.nationalarchives.gov.uk/{court}/data.ext?page=x
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/data.ext
- https://caselaw.nationalarchives.gov.uk/{year}/data.ext
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}]/{year}/data.ext
- https://caselaw.nationalarchives.gov.uk/{judgment-date}/data.ext
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/]/{judgment-date}/data.ext
- https://caselaw.nationalarchives.gov.uk/{court}[/{sub-division}/]{year}/{judgment-date}/data.ext

#### Examples

- https://caselaw.nationalarchives.gov.uk/ewca
- https://caselaw.nationalarchives.gov.uk/ewcop/data.feed
- https://caselaw.nationalarchives.gov.uk/uksc/data.html?page=2
- https://caselaw.nationalarchives.gov.uk/ewhc/comm
- https://caselaw.nationalarchives.gov.uk/ewch/pat/data.html
- https://caselaw.nationalarchives.gov.uk/2021
- https://caselaw.nationalarchives.gov.uk/ewhc/admin/2020/data.feed
- https://caselaw.nationalarchives.gov.uk/2021-05-01
- https://caselaw.nationalarchives.gov.uk/2019-13-14/data.html
- https://caselaw.nationalarchives.gov.uk/ewfc/2021-08-17
- https://caselaw.nationalarchives.gov.uk/ewhc/ipec/2018-01-27/data.feed
- https://caselaw.nationalarchives.gov.uk/ewca/civ/2019/2019-10-16
- https://caselaw.nationalarchives.gov.uk/ewhc/2018/2015-03-05/data.feed?page=7

## Consequences

The specification defines various future extensions - see that document for details.
