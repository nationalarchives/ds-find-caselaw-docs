# 8. How FRBRdates are managed and the current state of the FRBR model

Date: 2022-08-08

## Status

Accepted

## Context

The [Akoma Ntoso](http://www.akomantoso.org/) XML [spec](https://github.com/oasis-open/legaldocml-akomantoso/blob/master/csprd02-part2-specs/csprd02-part2-specs-schemas/akomantoso30.xsd)
provides room for a large number of different dates for each of the different FRBR representations of the document.

At this time our model is not as complicated, leading to challenges when we don't know what we can assume about the structure of the dates we might encounter in the documents we generate.

[Respect and maintain the FRBRdate attribute name in FRBRWork](https://github.com/nationalarchives/ds-caselaw-custom-api-client/pull/62) highlighted the need to document the current
state of what dates we are using and how we use them.

The discussion of this data and what it means which lead to this ADR are [on slack](https://dxw.slack.com/archives/C02TP2L2Z0F/p1659962075490729)

If the concepts of Work/Expression/Manifestation/Item nomenclature are new to you, there is [an excellent presentation](https://www.railslibraries.info/system/files/Anyone/mtg/2018/2018-08-20/152953/Updated%20Slides%20for%20WEMI%20webinar.pdf). FRBR, WEMI are both good search terms.

### A Joint Work/Expression date

We do not yet draw a distinction in the XML document between the date that a judgment was created (FRBRWork) and any later date that the judgments text was edited (FRBRExpression),
although the content hash indicates that we do place some distinction on this. As such, we have a single date for both these tags, which is perfectly ambiguous as to whether 
it reflects the initial version or any amended version.

The name attribute of these field may be `judgment` or `decision`, reflecting the nature of the document (this value is also found as the `name` attribute of the `judgment` tag)
but this historical separation is unhelpful when we wish to draw parallels between the two document types. Future work may wish to use a different common term for the dates, or
reflect the different meanings of these dates.

The name may also be "dummy", if the parser failed to extract a date. This is a placeholder used to ensure compliance with the Akoma Ntoso spec.

### Multiple Manifestation dates

The FRBRManifestation section may have multiple FRBRdate tags reflecting the creation of the XML document etc. from the words of the judgment or decision. These will typically be set by
processes under National Archives control (e.g. the transformation engine, the improvement engine); these aren't anything to do with the above.

## Decision

At this time:

`FRBRWork` and `FRBRExpression` MUST have exactly one `FRBRdate` child element. The `date` attributes of these `FRBRdate` elements MUST be identical.
The `name` attributes of these elements SHOULD be identical to the `name` attribute of the `judgment` element but SHOULD NOT be relied upon for any purpose.
The name attribute of 'dummy' SHOULD be replaced with the value of the `name` attribute of the `judgment`.

Functions that read the date can read either; functions that set the date MUST set both `date`s to the same value.

## The future

We are aware that we will need to re-evaluate this in the future: we will need the capability to handle different versions of the judgment/decision, and that at that point these dates will
differ to each other (with the Expression date perhaps being later?). We probably should use terms that do not draw a distinction between judgments and decisions, but instead draw
distinctions between initial handing down and revised versions (exact details will require consultation).

## Consequences

This shared understanding should bring into focus any omissions in this process and serve as a catalyst for future change.
