# 21. Additional metadata fields for backlog judgments

Date: 2025-05-12

## Status

Draft

## Context

Up to now, our parser has converted new court judgments from Word format (.docx) into Akoma Ntoso, an XML schema for legal documents. It attempts to identify key information in the body of the judgment and tags it with semantic inline elements. Sometimes, when the schema requires or when the body elements do not suit our needs, the parser also duplicates this information in the metadata header. But other times, when the body elements are sufficient, it does not. For example, we can search documents based on values in inline elements, so search optimization alone is not a reason to copy data to the metadata header.

Furthermore, sometimes we need information in the metadata block, but the schema does not provide any native markup for the values we have. The Akoma Ntoso schema has a `<proprietary>` element in its metadata block, into which we can put custom elements.

Recently, we have been asked to publish old documents, some of which are available in Word format, but others are available only in PDF. For the Word documents, we parse them as usual. For the PDFs, we do not attempt to extract any text; rather, we create an XML stub containing only metadata.

For these older documents, we also receive separate metadata files containing information about each document. We want to incorporate that metadata into the XML. For PDF documents, this external metadata is the only metadata we will have. But for old Word documents, we will have two sources of metadata: the _internal_ metadata our parser identifies through its normal process and the _external_ metadata we have been given.

## Decision

We will expand our use of the Akoma Ntoso `<proprietary>` element to store additional metadata for backlog judgments.

### Proprietary Metadata Elements

We will use the following elements within the `<proprietary>` block:

```xml
<proprietary xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
    <uk:court/>                 <!-- 0 or 1 -->
    <uk:year/>                  <!-- 0 or 1 -->
    <uk:number/>                <!-- 0 or 1 -->
    <uk:cite/>                  <!-- 0 or 1 -->
    <uk:summaryOf/>             <!-- 0 or 1 -->
    <uk:summaryOfCite/>         <!-- 0 or 1 -->
    <uk:caseNumber/>            <!-- 0 or many -->
    <uk:jurisdiction/>          <!-- 0 or 1 -->
    <uk:party role=""/>         <!-- 0 or many -->
    <uk:category parent=""/>    <!-- 0 or many -->
    <uk:sourceFormat/>          <!-- 0 or 1 -->
    <uk:parser/>                <!-- 1 -->
    <uk:hash/>                  <!-- 1 -->
    <uk:tna-enrichment-engine/> <!-- 0 or 1 -->
</proprietary>
```

Elements MUST appear in the order listed above. Some elements may be omitted if not applicable, but the relative order of included elements must be maintained.

### Element Definitions

**Original Elements:**

The following elements have been in use for some time:

- **uk:court** - A code designating the court that issued the judgment or decision. Example: `<uk:court>UKFTT-GRC</uk:court>`. Can be missing if the court is unknown. If present, its value will be one of a list of enumerated values. This code was created by us; it does not appear in the text.

- **uk:year** - The year as defined in the judgment's NCN, where extracted. Example: `<uk:year>2025</uk:year>` where the NCN is `[2025] UKSC 1`. Can be missing if NCN not extracted. If present, its value will be a four-digit integer. Note this is not always the same year as the judgment's handed-down date. Rarely, in the early days of January, a judgment will be numbered based on the prior year. Extracted for efficient search indexing.

- **uk:number** - The number of the judgment, assigned by the court. Unique within a court and year. Used for sorting. Example: `<uk:number>1</uk:number>`. Can be missing if there's no NCN. If present, its value will be an integer. A component of the judgment's Neutral Citation Number; extracted here for efficient search indexing.

- **uk:cite** - The Neutral Citation Number of the judgment or decision, assigned by the court. Example: `<uk:cite>[2025] UKSC 1</uk:cite>`. Can be missing if there's no NCN. Although this is also marked up in the body of the text, we duplicate it here because occasionally there are punctuation errors in the body, and we want a normalized form here.

- **uk:summaryOf** - The URI of the judgment summarized by this press summary. Example: `<uk:summaryOf>https://caselaw.nationalarchives.gov.uk/id/uksc/2025/18</uk:summaryOf>`. Only present in press summaries. Can be missing if not known.

- **uk:summaryOfCite** - The Neutral Citation Number of the judgment summarized by this press summary. Example: `<uk:summaryOfCite>[2025] UKSC 18</uk:summaryOfCite>`. Only present in press summaries. Can be missing if not known.

- **uk:jurisdiction** - A code indicating the subject matter of the case over which the court has jurisdiction. Example: `<uk:jurisdiction>InformationRights</uk:jurisdiction>`. Currently used only for the General Regulatory Chamber. Can be missing if not known. Currently there will never be more than one of these elements, although it is conceivable we may want to allow multiple values in the future.

- **uk:parser** - The version of the parser used to generate the XML. Example: `<uk:parser>0.22.1</uk:parser>`. Should always be present.

- **uk:hash** - The hash of the document's contents. Example: `<uk:hash>addee6a43d69dee4e62c9ccbf27df98874b4967a385397bed610cc414ee45c84</uk:hash>`. The SHA-256 hash of the document text with all whitespace removed.

- **uk:tna-enrichment-engine** - The version of the enrichment engine used to identify references within the body of the XML.

**New Elements:**

We will introduce the following additional elements for backlog documents:

- **uk:caseNumber** - A case number assigned by the court. Example: `<uk:caseNumber>2001/2/RTR</uk:caseNumber>`. Can be missing. There can also be more than one, as some judgments relate to more than one case.

- **uk:party** - A name of one of the parties in the case, and optionally the role played. Example: `<uk:party role="Claimant">Rosecal &amp; Co Law Firm</uk:party>`. May not exist if not extracted. May be more than one.

- **uk:category** - The name of a category, assigned by the court, and optionally the name of a parent category, if the category is a subcategory. Example: `<uk:category parent="Some Parent">Refusal to register</uk:category>`. May be none, many courts don't have categories. The `parent` attribute is optional.

- **uk:sourceFormat** - The MIME type of the source document. Example: `<uk:sourceFormat>application/vnd.openxmlformats-officedocument.wordprocessingml.document</uk:sourceFormat>`. Currently added only for backlog judgments.

### Element Usage Notes for each Type of Document

1. **New documents in Word format (no external metadata)**

   - Contain the original proprietary fields, if the parser can identify them
   - Do not contain `<uk:caseNumber/>`, `<uk:party/>`, `<uk:category>` or `<uk:sourceFormat/>`
   - Party names (`<party>`) and case numbers (`<docketNumber>`) are marked up in the body text only

2. **Old documents in PDF format (with external metadata)**

   - May contain some or all of the proprietary fields, if the information was provided in external metadata
   - No body text markup will be present

3. **Old documents in Word format (with external metadata)**
   - May contain some or all of the proprietary fields
   - May include both proprietary metadata elements AND body text markup for the same information
   - For example, if the parser identifies a party name in the body, it will mark it in place, but if the party name was also provided in the external metadata, the external value will appear in the proprietary section

## Considerations

- We could add a `<uk:sourceFormat/>` element to new judgments, or we could move this information to the JSON metadata for backlog judgments.
- We could add a `source` attribute to some proprietary elements, to indicate the provenance of the value.
- We could use the `<uk:caseNumber/>` and `<uk:party/>` elements also for new judgments, duplicating information for consistency with backlog document.
