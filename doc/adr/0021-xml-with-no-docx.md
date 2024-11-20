# 21. XML with no docx

Date: 2024-11-20

## Status

Draft

## Context

We need to support documents which do not have a source DOCX. They will typically be PDF-only, although we're imagining there might be other formats (zip files full of jpegs).

These documents might not have neutral ciation numbers -- this is outside the scope of this document.

## Decision

The parser will emit an XML document similar to what is currently provided, but with some differences to support the lack of high-quality formatting data

### Structurally valid (modified) AkomaNtoso

The emitted XML will validate against our modified AkomaNtoso schema

### Search Compatible External Metadata

Metadata is provided to the parser via spreadsheets. We will want to preserve some of this data.

The existing tag names (see the appendix) will be used inside a `uk:external-metadata` tag in the `proprietary` tag to allow this metadata to be searched at the same time as other documents that have these tags in the running body of the judgment. Values MUST NOT be deliberately replicated across `external-metadata` and other places, but MAY be replicated if the text body is successfully parsed and the string appeared in externally provided data sources.

Editors SHOULD be able to edit the external metadata and the Editor UI have affordances to do so.

### Marked as Low Quality

The `proprietary` tag will contain a `uk:source-document` tag, with attributes:

TODO: I think this part wants tearing apart carefully.

Each of these metrics defaults to `1`: we have no reason to doubt the quality of the document. Values of `0` imply a complete lack of quality, or an absence of that feature. Values below `0.5` should be considered poor, and mitigations applied. Values above `1` might be signs of additional verification.

- `uk:markup-quality-score`: Is the body of the document marked up well with appropriate HTML and AkomaNtoso tags?

- `uk:text-quality-score`: Are all the words believed to be in the right order, with appropriate interword spacing? (Linebreaks optional)

- `uk:parsed-format`: default `docx`, even if the docx isn't original. `pdf` an obvious value.

The tag SHALL contain human-readable text warning that the XML is low quality and should not be relied upon.

### Purposes for Low Quality Marks

#### Deprioritised in Search

Since the risk of documents having bad search experiences due to broken OCR / text flow issues, documents with low quality scores should be deprioritised in search.

#### Rejected for Impossible Tasks

Documents with no DOCX cannot be reparsed, so SHOULD be excluded from the list of reparse candidates, SHOULD not be reparsable in the UI and MUST not be sent for reparsing.

#### Hidden Information

The Public UI WILL NOT reveal the body of the XML, including HTML transforms, to users who have not opted in to recieving a poor quality document. It may reveal suitable subsections.

#### Warning the user

The PUI MAY flag that a document exists only as a PDF so they are not surprised by the absence of a HTML version.

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
