# Document metadata

This document lists all the types of metadata which can be associated with a document, if that metadata exists at the level of document, submission or version, how to access that metadata, how that metadata is sourced, and if that metadata should be considered editable.

<!-- Begin document metadata table -->
<!-- Generated from scripts/build_document_metadata_table using scripts/document-metadata.yml. Do not edit manually. -->

## Summary

| Name                                                                                                                    | Level                                      | Sourced from                                                | Editable | Multiple | Implemented |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------- | -------- | -------- | ----------- |
| [Case number](#metadata-casenumber)                                                                                     | Document body                              | Parser (Document body)<br>Metadata file                     | No       | No       | Yes         |
| [Categories](#metadata-categories)                                                                                      | Document body                              | Parser (Document body)<br>Metadata file                     | No       | No       | Yes         |
| [Court](#metadata-court)                                                                                                | Document body                              | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         |
| [Document first ingested after latest publication at](#metadata-documentfirstingestionafterlatestpublicationdatetime)   | Document properties                        | Parser (TDR metadata)                                       | No       | No       | No          |
| [Document first ingested at](#metadata-documentfirstingestiondatetime)                                                  | Document properties                        | Parser (TDR metadata)                                       | No       | No       | No          |
| [Document first published at](#metadata-documentfirstpublisheddatetime)                                                 | Document properties                        | EUI<br>Ingester                                             | No       | No       | Yes         |
| [Document first submitted after latest publication at](#metadata-documentfirstsubmissionafterlatestpublicationdatetime) | Document properties                        | Parser (TDR metadata)                                       | No       | No       | No          |
| [Document first submitted at](#metadata-documentfirstsubmissiondatetime)                                                | Document properties                        | Parser (TDR metadata)                                       | No       | No       | No          |
| [Document most recently ingested at](#metadata-documentlatestingestiondatetime)                                         | Document properties                        | Parser (TDR metadata)                                       | No       | No       | No          |
| [Document most recently published at](#metadata-documentlatestpublisheddatetime)                                        | Document properties                        | EUI<br>Ingester                                             | No       | No       | Yes         |
| [Document most recently submitted at](#metadata-documentlatestsubmissiondatetime)                                       | Document properties                        | Parser (TDR metadata)                                       | No       | No       | No          |
| [Identifiers](#metadata-identifiers)                                                                                    | Document properties                        | Ingester<br>EUI                                             | Yes      | Yes      | Yes         |
| [Judges](#metadata-judges)                                                                                              | Document body                              | Parser (Document body)<br>Metadata file<br>Stub form        | No       | Yes      | Yes         |
| [Judgment date](#metadata-date)                                                                                         | Document body                              | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         |
| [Jurisdiction](#metadata-jurisdiction)                                                                                  | Document body                              | Parser (Document body)                                      | No       | No       | Yes         |
| [Name](#metadata-name)                                                                                                  | Document body                              | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         |
| [NCN](#metadata-cite)                                                                                                   | Document properties, document body         | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         |
| [Parties](#metadata-parties)                                                                                            | Document body                              | Parser (Document body)<br>Metadata file                     | No       | Yes      | Yes         |
| [Source email](#metadata-sourceemail)                                                                                   | Document properties (should be Submission) | Parser (TDR metadata)                                       | No       | No       | Yes         |
| [Source name](#metadata-sourcename)                                                                                     | Document properties (should be Submission) | Parser (TDR metadata)                                       | No       | No       | Yes         |
| [TDR reference](#metadata-consignmentreference)                                                                         | Document properties (should be Submission) | Parser (TDR metadata)                                       | No       | No       | Yes         |
| [URI](#metadata-uri)                                                                                                    | Document object (inherent property)        | System                                                      | No       | No       | Yes         |
| [Version annotation](#metadata-versionannotation)                                                                       | Version                                    | Ingester<br>Enrichment                                      | No       | No       | Yes         |

## Details

<a id="metadata-casenumber"></a>

### Case number

The case number for the case this document relates to.

| Level         | Sourced from                            | Editable | Multiple | Implemented | Access via                  |
| ------------- | --------------------------------------- | -------- | -------- | ----------- | --------------------------- |
| Document body | Parser (Document body)<br>Metadata file | No       | No       | Yes         | `Document.body.case_number` |

<a id="metadata-categories"></a>

### Categories

Categories under which this document falls

| Level         | Sourced from                            | Editable | Multiple | Implemented | Access via                 |
| ------------- | --------------------------------------- | -------- | -------- | ----------- | -------------------------- |
| Document body | Parser (Document body)<br>Metadata file | No       | No       | Yes         | `Document.body.categories` |

<a id="metadata-court"></a>

### Court

The court which published this document. "Court" here means "any body capable of issuing a legally binding decision".

| Level         | Sourced from                                                | Editable | Multiple | Implemented | Access via            |
| ------------- | ----------------------------------------------------------- | -------- | -------- | ----------- | --------------------- |
| Document body | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         | `Document.body.court` |

<a id="metadata-documentfirstingestionafterlatestpublicationdatetime"></a>

### Document first ingested after latest publication at

The date and time the first version of this document following the latest publication was ingested into FCL.

| Level               | Sourced from          | Editable | Multiple | Implemented |
| ------------------- | --------------------- | -------- | -------- | ----------- |
| Document properties | Parser (TDR metadata) | No       | No       | No          |

<a id="metadata-documentfirstingestiondatetime"></a>

### Document first ingested at

The date and time the first version of this document was ingested into FCL.

| Level               | Sourced from          | Editable | Multiple | Implemented |
| ------------------- | --------------------- | -------- | -------- | ----------- |
| Document properties | Parser (TDR metadata) | No       | No       | No          |

<a id="metadata-documentfirstpublisheddatetime"></a>

### Document first published at

The date and time the document was first published on Find Case Law.

| Level               | Sourced from    | Editable | Multiple | Implemented | Access via                          |
| ------------------- | --------------- | -------- | -------- | ----------- | ----------------------------------- |
| Document properties | EUI<br>Ingester | No       | No       | Yes         | `Document.first_published_datetime` |

<a id="metadata-documentfirstsubmissionafterlatestpublicationdatetime"></a>

### Document first submitted after latest publication at

The date and time the first version of this document following the latest publication was submitted through TDR.

| Level               | Sourced from          | Editable | Multiple | Implemented |
| ------------------- | --------------------- | -------- | -------- | ----------- |
| Document properties | Parser (TDR metadata) | No       | No       | No          |

<a id="metadata-documentfirstsubmissiondatetime"></a>

### Document first submitted at

The date and time the first version of this document was submitted through TDR.

| Level               | Sourced from          | Editable | Multiple | Implemented |
| ------------------- | --------------------- | -------- | -------- | ----------- |
| Document properties | Parser (TDR metadata) | No       | No       | No          |

<a id="metadata-documentlatestingestiondatetime"></a>

### Document most recently ingested at

The date and time the most recent version of this document was ingested into FCL.

| Level               | Sourced from          | Editable | Multiple | Implemented |
| ------------------- | --------------------- | -------- | -------- | ----------- |
| Document properties | Parser (TDR metadata) | No       | No       | No          |

<a id="metadata-documentlatestpublisheddatetime"></a>

### Document most recently published at

The date and time the document was most recently published on Find Case Law.

| Level               | Sourced from    | Editable | Multiple | Implemented | Access via                          |
| ------------------- | --------------- | -------- | -------- | ----------- | ----------------------------------- |
| Document properties | EUI<br>Ingester | No       | No       | Yes         | `Document.first_published_datetime` |

<a id="metadata-documentlatestsubmissiondatetime"></a>

### Document most recently submitted at

The date and time the most recent version of this document was submitted through TDR.

| Level               | Sourced from          | Editable | Multiple | Implemented |
| ------------------- | --------------------- | -------- | -------- | ----------- |
| Document properties | Parser (TDR metadata) | No       | No       | No          |

<a id="metadata-identifiers"></a>

### Identifiers

Identifiers for a document (NCN, FCLID etc) stored within the structured identifier system.

| Level               | Sourced from    | Editable | Multiple | Implemented | Access via             |
| ------------------- | --------------- | -------- | -------- | ----------- | ---------------------- |
| Document properties | Ingester<br>EUI | Yes      | Yes      | Yes         | `Document.identifiers` |

<a id="metadata-judges"></a>

### Judges

A list of the names of the judges (or equivalent for the body) involved in any particular case.

| Level         | Sourced from                                         | Editable | Multiple | Implemented |
| ------------- | ---------------------------------------------------- | -------- | -------- | ----------- |
| Document body | Parser (Document body)<br>Metadata file<br>Stub form | No       | Yes      | Yes         |

<a id="metadata-date"></a>

### Judgment date

The date the document was published, usually the date a decision was handed down.

| Level         | Sourced from                                                | Editable | Multiple | Implemented | Access via                              |
| ------------- | ----------------------------------------------------------- | -------- | -------- | ----------- | --------------------------------------- |
| Document body | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         | `Document.body.document_date_as_string` |

<a id="metadata-jurisdiction"></a>

### Jurisdiction

The jurisdiction of the court which this decision was made under

| Level         | Sourced from           | Editable | Multiple | Implemented | Access via                   |
| ------------- | ---------------------- | -------- | -------- | ----------- | ---------------------------- |
| Document body | Parser (Document body) | No       | No       | Yes         | `Document.body.jurisdiction` |

<a id="metadata-name"></a>

### Name

The title of the document as most commonly used by humans. This _may_ vary from the exact title in the document text, for example by standardising casing.

| Level         | Sourced from                                                | Editable | Multiple | Implemented | Access via           |
| ------------- | ----------------------------------------------------------- | -------- | -------- | ----------- | -------------------- |
| Document body | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         | `Document.body.name` |

<a id="metadata-cite"></a>

### NCN

Where present, this document's Neutral Citation Number. This is a special case of identifier, which we actually want to deprecate.

| Level                              | Sourced from                                                | Editable | Multiple | Implemented | Access via                                              |
| ---------------------------------- | ----------------------------------------------------------- | -------- | -------- | ----------- | ------------------------------------------------------- |
| Document properties, document body | Parser (Document body)<br>Metadata file<br>EUI<br>Stub form | Yes      | No       | Yes         | `Document.identifiers.preferred(NeutralCitationNumber)` |

<a id="metadata-parties"></a>

### Parties

A list of the names of the parties involved in any particular case. This does _not_ include structured data on the nature of the party (eg defendant/appellant).

| Level         | Sourced from                            | Editable | Multiple | Implemented |
| ------------- | --------------------------------------- | -------- | -------- | ----------- |
| Document body | Parser (Document body)<br>Metadata file | No       | Yes      | Yes         |

<a id="metadata-sourceemail"></a>

### Source email

The email address of the person who submitted the document.

| Level                                      | Sourced from          | Editable | Multiple | Implemented | Access via              |
| ------------------------------------------ | --------------------- | -------- | -------- | ----------- | ----------------------- |
| Document properties (should be Submission) | Parser (TDR metadata) | No       | No       | Yes         | `Document.source_email` |

<a id="metadata-sourcename"></a>

### Source name

The name of the person who submitted the document.

| Level                                      | Sourced from          | Editable | Multiple | Implemented | Access via             |
| ------------------------------------------ | --------------------- | -------- | -------- | ----------- | ---------------------- |
| Document properties (should be Submission) | Parser (TDR metadata) | No       | No       | Yes         | `Document.source_name` |

<a id="metadata-consignmentreference"></a>

### TDR reference

The TDR reference of the submission.

| Level                                      | Sourced from          | Editable | Multiple | Implemented | Access via                       |
| ------------------------------------------ | --------------------- | -------- | -------- | ----------- | -------------------------------- |
| Document properties (should be Submission) | Parser (TDR metadata) | No       | No       | Yes         | `Document.consignment_reference` |

<a id="metadata-uri"></a>

### URI

The unique identifier for the document.

| Level                               | Sourced from | Editable | Multiple | Implemented | Access via     |
| ----------------------------------- | ------------ | -------- | -------- | ----------- | -------------- |
| Document object (inherent property) | System       | No       | No       | Yes         | `Document.uri` |

<a id="metadata-versionannotation"></a>

### Version annotation

A (hopefully) structured JSON blob describing how and why a new version of a document came into being.

| Level   | Sourced from           | Editable | Multiple | Implemented | Access via            |
| ------- | ---------------------- | -------- | -------- | ----------- | --------------------- |
| Version | Ingester<br>Enrichment | No       | No       | Yes         | `Document.annotation` |

<!-- End document metadata table -->
