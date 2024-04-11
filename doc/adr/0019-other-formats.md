# 19. Other Formats

Date: 2024-04-11

## Status

Draft

## Context

### The problem

Some court judgments are not received as **DOCX** files. The source document (also referred to as "payload" and "docx" in the code) might be:

- another form of word document [Rich Text Format (**RTF**), pre-2007 Word **doc** files, LibreOffice **odt** files]
- the best source document that exists is a **pdf** file, because the original born-digital file is lost, or it never existed digitally
- not currently available to Find Case Law (a number of judgments imported at the start of the process do not have associated word documents stored in S3 at the moment)
- other formats might exist -- e.g. a zip of jpegs of a scanned book but are outside the scope right now, and can probably be given a new unique extension.
- we consider audio or video to be out of scope at this time.

We assume in this discussion that the parser has somehow successfully generated XML, or a suitable placeholder which is otherwise acceptable to the Find Case Law team.

What impact would this have?

### Ingester

Currently the ingester detects the word document via the
[`metadata["parameters"]["TRE"]["payload"]["filename"]`](https://github.com/nationalarchives/ds-caselaw-ingester/blob/5b4272d86e4d1fa07285560a152ef219be76492d/ds-caselaw-ingester/lambda_function.py#L213) key, where
`metadata` is the contents of the `metadata.json` file. Nothing at this stage explicitly states that it is a DOCX file, although we do assume that is a DOCX when we save it to S3 at a path like [`uksc/2023/1/uksc_2023_1.docx`](https://github.com/nationalarchives/ds-caselaw-ingester/blob/5b4272d86e4d1fa07285560a152ef219be76492d/ds-caselaw-ingester/lambda_function.py#L519), ignoring the original extension.

A large amount of code refers to this `payload` as a `docx`; changing it is probably unhelpful.

**Recommendation:** Preserve extensions when saving the payload/"DOCX" to S3.

**Alternative:** Save payload/"DOCX" to a neutral S3 pathname.

**Recommendation:** Carefully consider whether the advantages of renaming variables containing `docx` outweigh the costs.

### Editorial UI

Editors use the source document to ensure that the contents of the XML reflect the judgment as made by the judge.

Currently the editorial interface exposes a "download docx" button that links to the unpublished assets bucket via a signed link. Since we have no other source types at present, this is hard coded, [referring](https://github.com/search?q=repo%3Anationalarchives%2Fds-caselaw-editor-ui%20docx_url&type=code) to [`document.docx_url`](https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/b7864f56cc8c54f8e0b68cb506b2ddba48138519/src/caselawclient/models/documents.py#L317) which ultimately [relies upon the URI of the document and appending `.docx`](https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/b7864f56cc8c54f8e0b68cb506b2ddba48138519/src/caselawclient/models/utilities/aws.py#L95).

**Recommendation:** We should ensure the S3 filename of the source document can be determined. This might be by:

- using a neutral S3 key
- the parser saving it in the XML
- reading it from S3 by trying different possibilities
- saving it to the MarkLogic metadata

(The 'try everything in S3' approach does not feel like a good one. PDF should be last.)

### Data Reusers

Data reusers currently use the fact that they can URL-bash to get the source document.

**Recommendation:** Notify data reusers about whatever changes we make

**Recommendation:** If it can be made without offending stakeholders who object to the public availability of source documents, have a (poorly-documented?) endpoint that data reusers can get the file from easily (by, e.g. HTTP redirection).

### TDR Acceptance

There does not appear to be a need for clerks to be able to send non-DOCX files to us, with the possible exception that sending ODT files would potentially avoid many of the PDF formatting issues caused by mismatches in the Word / LibreOffice page layout algorithms.

[TDR can accept Open Document Text files](https://www.nationalarchives.gov.uk/information-management/manage-information/digital-records-transfer/file-formats-transfer/).

**Recommendation:** Only if and when all parties are amenable to it, permit submissions of ODT files via TDR.

### TRE Acceptance

It is not clear whether we can send non-DOCX files to be parsed or reparsed. It feels like TRE should not care and pass the document to the parser as an opaque file, but that might not be true.

**Recommendation:** Verify that sending a non-DOCX file to the parser via the eventhub is acceptable.

### Producing a PDF

Currently, a PDF is generated when a file ending in `.docx` appears in the S3 bucket via an SNS notification (i.e. this logic exists entirely in AWS). A PDF with a source of `custom-pdfs` is not overwritten.

LibreOffice should automatically support printing to PDF for any sensible office-document format without modification.

**Recommendation:** Extend the list of extensions that trigger PDF generation within those which are supported by LibreOffice. This must occur on an extension-by-extension basis.

## Files that aren't from Word Processors

### Native PDFs

There shouldn't be an issue with native PDFs being overwritten (as there shouldn't be another different source PDF.) There would potentially be duplication if there was a neutral source URL and PDFs were expected to be at `uksc/2024/1/uksc_2024_1.pdf`.

### No File

It'd be nice if in the no file case the DOCX button didn't show up / gave a nice warning, but that might be a lot of effort for existing files.

### Unexpected file

Currently, the file would be renamed to `.docx` in S3.

If we fix that, unexpected files would be saved to S3 but not PDF parsed (as the extension wouldn't match), and would be linked to in the Editorial interface (and presumably to data reusers). That seems like an acceptable set of events.

## Decision

**TODO**

The change that we're proposing or have agreed to implement.

## Consequences

**TODO**

What becomes easier or more difficult to do and any risks introduced by the change that will need to be mitigated.
