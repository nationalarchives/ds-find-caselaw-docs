# 54. Akoma Ntoso IRIs

Date: 2026-01-12

## Status

Accepted

## Context

TODO: ensure all links are to the 2019 document not 2016.

The AkomaNtoso IRI of a [Work](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/csprd02/akn-nc-v1.0-csprd02.html#_Toc447637027), [Expression](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/csprd02/akn-nc-v1.0-csprd02.html#_Toc447637028) or [Manifestation](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/csprd02/akn-nc-v1.0-csprd02.html#_Toc447637031) should be used within the XML markup, these are in sections 4.4-4.6

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

Note that for more complicated courts, the identifier used currently in the XML is formatted like `#ewhc-kbd-tcc`. This does not agree with the Neutral Citation. ⚠️ This might need resolving.

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

### Expression

TODO TODO TODO

### Manifestations

TODO TODO TODO

> Different Manifestations of the same Expression generated in different data formats will have different IRI references. All of them are all immediately derived from the baseline, which is the IRI for the Expression.

> The IRI for the Manifestation as a whole consists of the following pieces:
>
> - The IRI of the corresponding Expression as a whole
> - The markup authoring information (optional). [T]his value MUST correspond to the content of element <FRBRauthor> in the <FRBRManifestation> section of the metadata.
> - Any relevant markup-specific date (optional). [T]his value MUST correspond to the content of element <FRBRdate> in the <FRBRManifestation> section of the metadata.
> - Any additional markup-related annotation (e.g., the existence of multiple versions or of annotations.) (optional)
> - The character “`.`” (required)
> - A unique three or four letter extension signifying the data format in which the Manifestation is drafted (required). [e.g. “pdf”, “doc”, “docx”, “htm”/“html”;] “xml” for an XML Manifestation, or “akn” for the package of all documents including XML versions of the main document(s) according to the Akoma Ntoso vocabulary. For an Akoma Ntoso XML representation, this value MUST correspond to the content of element <FRBRformat> in the <FRBRManifestation> section of the metadata.

Some examples:

– [http://www.authority.org]/akn/dz/debaterecord/2004-12-21/fra@.doc
Word version of the Algerian parliamentary debate record, 21st December 2004, Original French version

– [http://www.authority.org]/akn/sl/act/2004-02-13/2/eng.pdf
PDF version of the Sierra Leone act number 2 of 2004, English version, current version (as accessed today)

– [http://www.authority.org]/akn/sl/act/2004-02-13/2/eng@2004-07-21.akn
Package of all documents in Akoma Ntoso XML of the Sierra Leone act number 2 of 2004. English version, as amended in July 7th 2004.

– [http://www.authority.org]/akn/sl/act/2004-02-13/2/eng@2004-07-21/CIRSFID/2011-07-15.akn
Package of all documents including XML versions of the Sierra Leone enacted Legislation. Act number 2 of 2004. English version, as amended in July 2004. Rendered in Akoma Ntoso by CIRSFID on 15 July 2011.

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

We could use `court` or `tribunal`. But

> the naming of entities should not depend on the presence or absence of a given class except for TLC. This means that it is necessary that each instance of each TLC is provided with an ID string that is guaranteed to be unique within the TLC.

The examples below don't describe the entities in further details, we shall emulate that behaviour.

> - - The ID of the instance, guaranteed to be unique within the TLC.

The [XML Vocabulary](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html) gives three examples:

```
<TLCOrganization href="/akn/us/ontology/organization/interAmericanCommercialArbitationCommission" showAs="Inter-American Commercial Arbitration Commission"/>

<TLCOrganization eId="house" href="/akn/us/ontology/organization/house" showAs="U.S. House of Representatives"/>

<TLCOrganization eId="olrc" href="/akn/us/ontology/organization/olrc" showAs="Office of the Law Revision Counsel"/>
```

We use a prefix `akn/gb/ontology/organisation/` and then strings like `uksc`, `ewhc-kbd-tcc`, `ewhc`, `ewhc-kbd`. We note that we cannot easily use NCN derived identifiers.

## Decision

The change that we're proposing or have agreed to implement.

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change that will need to be mitigated.
