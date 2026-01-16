# 54. Akoma Ntoso IRIs

Date: 2026-01-12

## Status

Accepted

## Context

TODO: ensure all links are to the 2019 document not 2016.

The AkomaNtoso IRI of a [Work](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html#_Toc531692270), [Expression](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html#_Toc531692271) or [Manifestation](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html#_Toc531692274) should be used within the XML markup, these are in sections 4.4-4.6

The AkomaNtoso IRIs of Works, Expressions and Manifestations are specified in sections 4.4-4.6 of the Akoma Ntoso Naming Convention 1.0.

### Work

The [Work IRI](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/csprd02/akn-nc-v1.0-csprd02.html#_Toc447637027) spec is abridged and annotated below.

> The IRI for the Work consists of the following pieces, separated by forward slashes “`/`”:
>
> - The base URL of a naming authority with IRI-resolving capabilities

This shall be `https://caselaw.nationalarchives.gov.uk`

> - A detail fragment that organizes additional data in a hierarchical fashion:
> - - The `/akn` prefix to allow the identification of the IRI as belonging to the Akoma Ntoso Naming Convention (required)
> - - Country or subdivision according to ISO 3166-1 or ISO 3166-2. This value MUST correspond to the content of the element `<FRBRcountry>` in the metadata. (required)

ISO 3166-1 would be `GB` or `gb` , and we shall use `gb` since the IRI examples in the AkomaNtoso spec use lower case exclusively in the country field.

[Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-2:GB) notes [ISO 3166-2](https://www.iso.org/obp/ui/#iso:code:3166:GB) has `GB-ENG`, `GB-NIR`, `GB-SCT` and `GB-WLS` for England, Northern Ireland, Scotland and Wales, that BS 6879 also supports `GB-CYM`. The ISO standard also 'notes for completeness' `GB-EAW` (England and Wales) which Wikipedia notes is used legislatively. This is additional complexity we do not need to engage with so long as the Scottish and England/Wales courts have different identifiers.

> - - Type of document. This value MUST correspond to the element immediately below the `akomaNtoso` root element (required)

The value of that element is `judgment` or `doc` for press summaries; we should use these.

> - - Any specification of document subtype, if appropriate. This value MUST correspond to the content of the element `<FRBRsubtype>` or, in its absence, to the “name” attribute of the document type (optional).

We do not use `FRBRsubtype`. The value of the name attribute is `judgment` for judgments or `pressSummary` for press summaries.

We should omit this section for judgments, as it is inappropriate. We should include this section for press summaries, as it is descriptive.

> - - The emanating actor, unless implicitly deducible by the document type (e.g., acts and bills do not usually require actor, while ministerial decrees and European legislation do). This value MUST correspond to the content of the element `<FRBRauthor>` in `<FRBRWork>` (optional).

The `FRBRWork/FRBRauthor` refers by reference (such as `href='#uksc'`) to a `TLCOrganization` with a matching `eId='uksc'` attribute. It has a `href` attribute pointing to the website and a human readable name in the `showAs` attribute.

Note that for more complicated courts, the identifier used currently in the XML is formatted like `#ewhc-kbd-tcc`. This does not agree with the Neutral Citation.

⚠️ We may need to make a decision about whether using the code (vs the param) make sense here. Params will need to have their slashes munged.

⚠️ It is not clear what 'correspond' means in this context.

> - - Original creation date (expressed in YYYY-MM-DD format or just YYYY if the year is sufficient for identification purposes). This value MUST correspond to the content of the element `<FRBRdate>` in `<FRBRExpression>` (required).

For items with NCNs, YYYY would be appropriate. For items without NCNs, the number is intended to be unique enough that YYYY is sufficent. Use YYYY.

> - - Number or title or other disambiguating feature of the Work (when appropriate, otherwise optionally the string nn). This value MUST correspond to the content of element `<FRBRnumber>` or `<FRBRname>` (required when necessary for disambiguation).

This should be the number at the end of an NCN, or `fcl.xxxxxxx`.

⚠️ This might imply that we should include FCL ids as `<FRBRnumber>`s

> - - Component and fragment specifications, as specified in sections 4.7 and 4.8 (optional)

These are outside the scope of this document; we do not yet have a sensible way of referring to subsections of a document.

Examples of work IRIs:

https://caselaw.nationalarchives.gov.uk/akn/gb/judgment/uksc/2024/1
https://caselaw.nationalarchives.gov.uk/akn/gb/doc/pressSummary/uksc/2024/1
https://caselaw.nationalarchives.gov.uk/akn/gb/judgment/uksc/2024/tna.htg4pyr2

### Courts

[Section 4.10 of the Naming Convention](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html#_Toc531692286) specifies (edited):

> The IRI for non-document entities consists of:

> - The base URL of a naming authority with IRI-resolving capabilities

`https://caselaw.nationalarchives.gov.uk`

> - A detail fragment organizing in a hierarchical fashion the additional data:
> - - The string “`/ontology`”
> - - The official name of the appropriate top level class (TLC).
>     TLCs include Work, Expression, Manifestation, Item, Person, Organization, Concept, Object, Event, Process, Role, Term and Location.

Use `Organization`, note spelling.

> - - Any number (including none) of slash-separated subclasses of the TLC, as long as they all refer to correct properties of the corresponding instance

We could use `court` or `tribunal`. But:

> the naming of entities should not depend on the presence or absence of a given class except for TLC. This means that it is necessary that each instance of each TLC is provided with an ID string that is guaranteed to be unique within the TLC.

Categorising things is hard (especially sub-court entities), and we can save significant complexity by omitting further optional categories. Note that the [XML Vocabulary](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html) gives three examples:

```
<TLCOrganization href="/akn/us/ontology/organization/interAmericanCommercialArbitationCommission" showAs="Inter-American Commercial Arbitration Commission"/>

<TLCOrganization eId="house" href="/akn/us/ontology/organization/house" showAs="U.S. House of Representatives"/>

<TLCOrganization eId="olrc" href="/akn/us/ontology/organization/olrc" showAs="Office of the Law Revision Counsel"/>
```

which have no additional subclasses; we shall copy this behaviour and use zero additional subclasses.

> - - The ID of the instance, guaranteed to be unique within the TLC.

The [XML Vocabulary](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html) gives three examples:

```
<TLCOrganization href="/akn/us/ontology/organization/interAmericanCommercialArbitationCommission" showAs="Inter-American Commercial Arbitration Commission"/>

<TLCOrganization eId="house" href="/akn/us/ontology/organization/house" showAs="U.S. House of Representatives"/>

<TLCOrganization eId="olrc" href="/akn/us/ontology/organization/olrc" showAs="Office of the Law Revision Counsel"/>
```

We use a prefix `akn/ontology/organisation/` and then strings like `uksc`.

For more complicated cases where the codes and params diverge (e.g. `ewhc-kbd-tcc` vs `ewhc/tcc`), if we used the param we would need to munge the `/`. If we're happy using the codes then that means we don't need to change the identifier at all.

`ewhc` would also be valid. The identifier doesn't explicitly encode the heirarchical nature of our naming, but that's okay.

## Decision

Use IRIs of the form:

```
https://caselaw.nationalarchives.gov.uk/akn/gb/judgment/uksc/2024/1
https://caselaw.nationalarchives.gov.uk/akn/gb/doc/pressSummary/uksc/2024/1
https://caselaw.nationalarchives.gov.uk/akn/gb/judgment/uksc/2024/tna.htg4pyr2
```

for works.

Use identifiers of the form

```
https://caselaw.nationalarchives.gov.uk/akn/ontology/organisation/ewhc-kbd-tcc
```

for courts, where the last segment is a court code.

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change that will need to be mitigated.
