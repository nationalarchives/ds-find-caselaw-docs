# 51. Capture additional provenance data via parser metadata file

Date: 2025-12-16

## Status

Accepted

## Context

As originally designed, the system primarily stores information about a document by embedding that information in the document XML itself - only limited amounts are stored as a sidecar in the [MarkLogic properties](https://docs.progress.com/bundle/marklogic-server-develop-server-side-apps-12/page/topics/properties.html). This means that we're unable to store additional information about the provenance of a document and its associated metadata, specifically:

- The type of file which is the most primary source
- The origin of that primary source
- If any additional metadata has been provided which isn't derived exclusively from that source
- If the XML document contains 'renderable' text.

All these pieces of information are now needed to better inform downstream decisions around processing and rendering steps, so we need to capture them. However, we do not want them captured in the XML which is made available to download.

## Decision

The parser will record necessary field values in the metadata JSON blob. These will then be extracted during the ingestion process and saved against the document as MarkLogic properties. A persistent record will also exist in the metadata JSON file should it be needed for audit purposes.

The data structure is intentionally richer than a simple key/value store so that it is extensible, since we may in future want to capture additional provenance information. These extensions are not covered in this ADR.

### JSON structure

These fields shall be in the JSON blob the parser outputs containing other metadata, under the `PARSER` key (values are examples):

```json
  "primary_source": {
    "filename": "document_filename.docx",
    "sha256": "4df616de1a40eca885fc0ccefcf15dbba80d431c3b3300b794bff2e68b78b2f7",
    "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "route": "BULK"
  }
```

```json
  "metadata_fields": [
    {
      "id": "640bc40d-77d2-4acb-8fee-84cbf8a9cfa7",
      "name": "neutral_citation_number",
      "value": "[2025] UKSC 123",
      "source": "document",
      "timestamp": "2025-12-17T18:00:00"
    },
    {
      "id": "18b39c0a-afc1-4a5d-b75b-9856c1ea53f2",
      "name": "title",
      "value": "A Misspelled Judgement",
      "source": "document",
      "timestamp": "2025-12-17T18:00:00"
    },
    {
      "id": "1f8756fa-d217-4a68-9abb-97808eef1770",
      "name": "headnote",
      "value": "An example of a headnote.",
      "source": "external",
      "timestamp": "2025-12-17T18:00:00"
    },
    {
      "id": "897fc8b6-7122-4343-ba03-334105ba5db5",
      "name": "category",
      "value": {
        "name": "Category One",
        "parent": null
      },
      "source": "external",
      "timestamp": "2025-12-17T18:00:00"
    },
    {
      "id": "ffe69bd7-d6b4-45d7-a367-777fb15424c4",
      "name": "category",
      "value": {
        "name": "Subcategory One",
        "parent": "Category One"
      },
      "source": "external",
      "timestamp": "2025-12-17T18:00:00"
    },
    {
      "id": "ea28c934-84db-447e-b891-14f315e647c8",
      "name": "title",
      "value": "A Misspelled Judgment",
      "source": "editor",
      "timestamp": "2025-12-17T18:00:00"
    }
  ]
```

```json
  "xml_contains_document_text": true
```

### MarkLogic structure

These fields will be stored in MarkLogic using a similar structure, each as top-level properties.

```xml
<primary_source>
	<filename>document_filename.docx</filename>
	<sha256>4df616de1a40eca885fc0ccefcf15dbba80d431c3b3300b794bff2e68b78b2f7</sha256>
	<mimetype>application/vnd.openxmlformats-officedocument.wordprocessingml.document</mimetype>
	<route>BULK</route>
</primary_source>
```

```xml
<metadata_fields>
  <metadata id="640bc40d-77d2-4acb-8fee-84cbf8a9cfa7" name="neutral_citation_number" source="document">[2025] UKSC 123</metadata>
  <metadata id="18b39c0a-afc1-4a5d-b75b-9856c1ea53f2" name="title" source="document">A Misspelled Judgement</metadata>
	<metadata id="1f8756fa-d217-4a68-9abb-97808eef1770" name="headnote" source="external">An example of a headnote.</metadata>
	<metadata id="897fc8b6-7122-4343-ba03-334105ba5db5" name="category" source="external">
    <name>Category One</name>
    <parent />
  </metadata>
  <metadata id="ffe69bd7-d6b4-45d7-a367-777fb15424c4" name="category" source="external">
    <name>Subcategory One</name>
    <parent>Category One</name>
  </metadata>
  <metadata id="ea28c934-84db-447e-b891-14f315e647c8" name="title" source="editor">A Misspelled Judgment</metadata>
</metadata_fields>
```

```xml
<xml_contains_document_text>true</xml_contains_document_text>
```

### Field descriptions

A full JSON Schema describing fields and possible values for the JSON blob from the parser will be created and stored centrally (location to be determined in a future ADR).

#### `primary_source`

This object shall describe the file which is the most primary source available to Find Case Law, collecting its filename, a SHA256 checksum of that file (for audit purposes), the MIME type of that file, and a short string describing the route taken to reach the parser (currently one of `TDR` or `BULK`). For documents created directly within the EUI (eg standalone PDF uploads) this may have a value in MarkLogic of `EUI`. This value could _hypothetically_ appear in metadata from the parser at a future date if we introduce reparse capabilities for PDF documents, but is not currently expected.

#### `metadata_fields`

A list of additional pieces of metadata which are associated with the document. These may come from multiple sources, currently expected to be `document` ("this information can be derived purely from the primary source"), `external` ("this information has been provided by a secondary source such as a CSV of document metadata"), or `editor` ("this information has been manually keyed in by an editor").

IDs are UUIDs which are unique to the combination of field, value and source (eg the same field from multiple sources should have differing UUIDs even if they agree on value) and exist to allow additional pieces of metadata to be interrogated and manipulated in future. IDs MUST be retained if metadata is passed through a process such as reparsing. Where an ID is not known a new UUID can be created.

This allows multiple fields with the same name by design; it is understood that there may be multiple claims about the same piece of metadata from different sources, and this can be accommodated. This ADR does _not_ set out any particular way of deciding on the precedence of conflicting metadata, as they should all be stored.

#### `xml_contains_document_text`

A boolean flag indicating if the XML is representative of the actual contents of the document (`true`) and as such can be rendered to view in a browser, or if instead it is just a placeholder for a document which is only available in another format (eg as PDF).

### Handling metadata in the reparse flow

Initially, documents with any metadata not derived from the document itself should be excluded from any reparsing behaviour. This is to prevent data loss where the below plan for round-tripping data hasn't been completed.

Ultimately, whenever a document is scheduled for re-parsing _all_ metadata should be provided as hints to the parser, as they may influence the code path the parser takes. The parser should return all metadata fields as provided, and where it has detected a change in value (for example where parser improvements have led to more accurate detection of an NCN) this should be added as a new piece of metadata. It will be the responsibility of a downstream process to decide on precedence.

## Consequences

- A full list of possible additional metadata fields currently in use will need to be compiled
- A JSON Schema describing the JSON metadata blob will need to be written, and placed in a location as determined by a future ADR.
- Reparsing processes will need to be modified to exclude documents either without a primary source, or with supplementary metadata
- We will need to update any document merge processes to make sure these fields are properly replaced or merged (as appropriate)
- HTML content detection will need to be modified to detect the presence of the 'renderable' text flag, instead of using an element-based heuristic
