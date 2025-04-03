# 21. XML format for documents where source text cannot be extracted by the parser

Date: 2024-11-20

## Status

Draft

## Context

We need to support documents where the structured contents of the document cannot necessarily be extracted by the parser. They will typically be PDF-only, although we're imagining there might be other formats (such as zip files full of jpegs).

These documents might not have neutral ciation numbers -- this is outside the scope of this document.

## Decision

The parser will emit an XML document similar to what is currently provided, but with some differences to support the lack of high-quality formatting data

### Structurally valid (modified) AkomaNtoso

The emitted XML will validate against our modified AkomaNtoso schema

### Search Compatible External Metadata

Metadata is provided to the parser via spreadsheets. We will want to preserve some of this data.

The existing tag names (see the appendix) will be used inside a `uk:external-metadata` tag in the `proprietary` tag to allow this metadata to be searched at the same time as other documents that have these tags in the running body of the judgment; however, `akn:` namespaced tags are forbidden, so the `uk:` namespace MUST be used instead.

Values MUST NOT be deliberately replicated across `external-metadata` and other places, but MAY be replicated if the text body is successfully parsed and the string appeared in externally provided data sources.

Editors SHOULD be able to edit these metadata values within the `proprietary` tag and the Editor UI have affordances to do so.

### Marked as Low Quality

The `proprietary` tag will contain a `uk:source-document` tag, containing two fractional attributes:

Each of these numerical metrics defaults to `1.0`: we have no reason to doubt the quality of the document. Values of `0.0` imply a complete lack of quality, or an absence of that feature. Values below `0.5` should be considered poor, and mitigations applied. Values above `1.0` might be signs of additional verification.

- `uk:markup-quality-score`: Is the body of the document marked up well with appropriate HTML and AkomaNtoso tags?

- `uk:text-quality-score`: Are all the words believed to be in the right order, with appropriate interword spacing? (Linebreaks optional)

There is also:

- `uk:source-document-format`: the MIME type of the document from which this XML was generated. For Rich Text
  documents, and others where the document was converted to docx first, the mime type still will be `application/vnd.openxmlformats-officedocument.wordprocessingml.document`;

- `uk:markup-human-reviewed`: boolean -- An editor has reviewed the document. This will not be added by any parser, but may be added in the EUI.

- `uk:quality-warning`: Human readable text warning that the XML is low quality and should not be relied upon.

### Purposes for Low Quality Marks

#### Rejected for Impossible Tasks

Documents with no DOCX cannot be reparsed via the existing framework, so SHOULD be excluded from the list of reparse candidates, SHOULD NOT be reparsable in the UI and MUST not be sent for reparsing.

Documents without text SHOULD NOT be sent to enrichment.

#### Hidden Information

The Atom Feed MAY allow searching for only documents with sufficient quality scores.

The Public UI SHOULD NOT attempt to display XML or HTML transforms of XML to users where the text and/or markup quality scores are insufficient. (0.5 is probably the threshold)

XML representations MAY be available to users who explicitly request them but SHOULD NOT be routinely displayed
in the PUI.

#### Warning the user

The Public UI SHOULD indicate to users that a document is not available as HTML and instead is only available
as the original source document (or other compiled artifact in the future)

### Mediocre-Effort Text

An attempt SHOULD be made to extract full text from the document to support full text search. The parser MAY mark it up beyond the minimum to achieve AkomaNtoso compliance, but this is not expected. The parser MAY identify output which contains a high-proportion of non-words, and SHOULD emit no text if the text quality is sufficiently poor, and will have to do so if there is no text available.

## Consequences

- Full text search preserved
- Bad data not shown to users
- Search experience preserved

---

## Appendix: Current Search XPATH

### Party

element word query on `akn:party` OR

element attribute word `akn:FRBRname/@value`

### Court

element value query on `judgments:court` (!) OR

element value query on `uk:court` OR

element attribute word query on `akn:FRBRuri/@value`

### Judge

element word query on `akn:judge`

### Dates from/to

path range query on `akn:FRBRWork/akn:FRBRdate/@date`

### Neutral Citation

element value query on akn:cite

### Keyword

word query, unstemmed, anywhere?

### Display

```akn:proprietary/uk:court
akn:proprietary/uk:year
akn:FRBRWork/akn:FRBRdate
akn:FRBRWork/akn:FRBRname
uk:cite
akn:neutralCitation
uk:court
uk:jurisdiction
uk:hash
akn:FRBRManifestation/akn:FRBRdate
```
