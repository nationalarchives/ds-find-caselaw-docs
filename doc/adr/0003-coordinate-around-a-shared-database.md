# 3. Coordinate around a shared database

Date: 2022-02-04

## Status

Accepted

## Context

The system is primarily concerned with managing the creation and maintenance of
a corpus of LegalDocML documents.

Various microservices need to work with the data in this form, including:

* Public Access UI (read-only)
* Administration UI (read-write)
* Validation engine (read-write)
* Enrichment engine (read-write)

## Decision

All microservices will use LegalDocML documents stored in a shared, central MarkLogic
database.

Services MAY NOT communicate LegalDocML documents to each other in any way, other
than storing them in this shared database, and perhaps notifying each other that database
content has been changed (to be detailed in future as required).

Services in the transformation pipeline responsible for creating LegalDocML from other
formats MAY communicate in other ways, but that is beyond the scope of this ADR. Once those
documents are in a form that can be stored in MarkLogic, that should be the only transfer
mechanism.

![Container Diagram of database pattern](https://www.plantuml.com/plantuml/png/VP9FivCm5CNtV8fODpZZAnjNhXu2u-j8RQSK7LTCIAuGpHyc2LM_lJUrfQ3rxJBd_ixzSoQFpbFhHoL9z49e9aSEfFT-S6-JnD8VwqxuVcn71vOPxK7xDJCg6IJLmVJWF9UYJR8t3_iWrTioKTHvi2Wr6Jgeq63N0x9HLAPVTlMnIQkc-b0SiwVuLHHLlv1MJV7Jnq9tuBmm-ZLPRQxl5J9JdzXRgjrNOnKDjK9tg29zNCZaZxx2GlOI_JVxYKh1gJSMIv-kxy1Lh0Sqsp3lib8CsWhMApnvcbDC4gd0dWI3HNlAbT32uPANAzA5GEfDc9L_exep2-CmjbAmUeFL_Vb9KiR0kRyTDqlUnehQxwNf14EYX8xAtB1jIRXXutb3XxUTGzXUmT3X078Uz7y2jS10dC1DtHnwW_K-Fr-5MQ0U0lzEe6EU-HmR1px7ciETl9_Zot_Ila-75MQLMT8MA0z4zRJxt9J5--9ZZX_o4JJ7p_eR)

## Consequences

Individual microservices may need their own database to store extra information
that is not related to specific documents. This ADR does not preclude the creation
of such databases.
