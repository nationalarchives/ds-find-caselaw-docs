# 17. pseudo NCNs

Date: 2024-04-24

## Status

in Review

## Context

Many judgments in the body of UK case law do not have Neutral Citation Numbers (NCNs). These include:

- Judgments that predate the issuance of NCNs, potentially going back centuries.

- Judgments from lower courts that do not issue NCNs including BAILII issued IDs.

- Judgments intentionally not given an NCN, because they’re not intended to be cited.

- Judgments that are parsed incorrectly, and have either an incorrect or missing NCN. _Note: this last category of document will not be included in our pseudo NCN MVP_

The Find Case Law service needs to be able to include these judgments which do not have and never will have a court issued NCN. We need to fit them into our URL scheme, which is currently based on the structure of the NCN (see [ADR 4, “Adopt a standardised URL scheme”](https://github.com/nationalarchives/ds-find-caselaw-docs/blob/main/doc/adr/0004-adopt-a-standardised-url-scheme.md)) but modifies this exisiting scheme laid out in ADR4.

Therefore, we need to give these judgments our own identifier [TNA ID] and generate URLs with them.

ADR #4 includes URLs for TNA ordinal numbers, though does not define exactly what they are.

An estimated [3.5 million cases](https://commonslibrary.parliament.uk/research-briefings/cbp-8372/) entered courts and tribunals in 2021 in our jurisdiction. We don’t need to allocate identifiers to all of these, only those with no court issued NCN, but our scheme should take this figure into account. It’s possible that this will increase significantly in the future, with novel legal approaches such as AI litigation, etc, so we should give ourselves some room for expansion.

## Decision

As well as any court issued true NCN they may come with, we will aim to issue all judgments a pseudo-NCN which would be cited in the following format:

Citation `[{year}] {court code} {namespace}.{id}`

As with a true NCN, the court code and year come first, but the ordinal number is replaced with a combination of a namespace followed by a unique alphabetical ID.

For the first piece of work the court code and year are not optional. The ids are unique per year and court as with normal NCN ordinals.

In the future if we expand the scope of our pseudo-NCNs to assign them to every document, the court code and year would be optional but the id itself would be universally unique in our system. If the judgment does not come with a pre-issued NCN, we will consider our pseudo-NCN to be the canonical identifier for the purposes of database storage, etc.

## Namespace

We will use the namespace `tna` for identifiers that we issue.

## ID

The ids will be issued sequentially as numbers and converted to a string of consonants using the [SQID](https://sqids.org/nim) library.

This will allow us to ensure we do not duplicate ids (the ordinal progression) however users will not confuse our id for an NCN nor look for items missing in a sequence because they will appear as letters.

The SQID will be four characters long, all letters, no vowels (a,e,i,o,u,y) and no upper case. This will give us up to 160,000 ids per court per year. If we need more than this we can add an fifth character to the SQID.

The format of the namespace and ID is chosen specifically for compatibility with ECLI, which allows "ordinal” numbers which are alphanumeric and can contain dots.

## Examples of pseudo-NCN citations

URL `ukhl/1932/tna.xkcd`

Citation `[1932] UKHL tna.xkcd`

Or, in ECLI form:

`ECLI:UK:UKHL:1932:tna.xkcd`

## URIs

ADR #4 defines URLs for TNA-issued ordinal numbers. This ADR amends that scheme to replace the `num` part of the URL with the namespace component defined above. Judgments identified by pseudo-NCNs will therefore have work URIs of the following form:

`https://caselaw.nationalarchives.gov.uk/id/{court}/[{sub-division}/]{year}/{namespace}.{id}`

For example:

`https://caselaw.nationalarchives.gov.uk/id/UKHL/1932/tna.xkcd`

Expression and manifestation URIs follow suit, in the same equivalent patterns defined in ADR #4. For example:

`https://caselaw.nationalarchives.gov.uk/UKHL/1932/tna.xkcd`

`https://caselaw.nationalarchives.gov.uk/UKHL/1932/tna.xkcd/data.xml`

Out of scope for initial implementation but if the court and year are unknown, the expression URL would have the namespace at the root:

`https://caselaw.nationalarchives.gov.uk/tna.mqbqm.kzkkt`

## Consequences

This scheme does not produce obviously ordered numbers for cases. We are not expecting to be able to ingest judgments in a known order, so we cannot know the ordering of cases without extensive human research. We could allow alternative identifiers to be stored in the database and used in URLs, so that friendlier identifiers can be added later by hand. This is outside the scope of using TNA ids to publish judgments without NCNs.

A true court issued NCN can be considered a pseudo-NCN with an empty namespace (and therefore no dot), and where the ids are monotonically-increasing ordinal decimal integers rather than sqids.

To represent BAILII-issued NCNs as an alternative (e.g. for search purposes), we should scope it into a bailii namespace; for example `[1932] UKHL bailii.100`.

In future work where we want to use TNA ids to identify documents as they come in, we may want to change the identifier that we consider canonical. For instance, we may initially only have a pseudo-NCN that we issue, but an NCN may be minted later on.

## Tasks

- [x] Catherine/Jim/John/Nicki: decide on namespace prefix - TNA has been decided on

- [/] Commit ADR to GitHub repo - in progress

- [ ] Devs: Generate sqid for each sequential document when an editor pushes the 'sqid' button, and thence generate a pseudo-NCN for every incoming document with no NCN.

- [ ] Devs: Store documents in ML which don’t have a court-issued NCN using our pseudo-NCN generated by the editors as the primary identifier.

- [ ] UR/UX Decide if/how these are displayed on the Public UI - will they be displayed where court issued NCN's appear?

- [ out of scope for MVP] Devs: Find an alternate way to generate sqid without duplicates for documents which Jim will auto-publish from the backlog

- [out of scope for MVP] Jim: extend judgment XML schema to allow multiple identifiers so that we can embed our identifiers as well as the official NCN. Probably involves putting the `<uk:xxx>` tags into a container tag which can be repeated, but Jim is the expert here.
