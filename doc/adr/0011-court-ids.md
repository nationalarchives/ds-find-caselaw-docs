# 11. Court IDs

Date: 2022-11-16

## Status

Draft (**TODO** change to `Accepted`)

## Context

The court system is complicated, and sometimes only has a close mapping to Neutral Citations.

Notable complications are:

[2011] EWHC 90218 (Costs) and [2022] EWHC 1609 (SCCO) refer to the same court, the Senior Courts
Costs Office (of the High Court)

[2021] EWHC 79 (QB) and [2022] EWHC 2891 (KB) refer to the same court, which is variously known
as the Queen's or King's Bench Division

[2022] EWHC 2832 (Admin) is a Divisional Court judgment, but the court is indistinguishable by
Neutral Citation from the Administrative Court judgment [2022] EWHC 2882 (Admin).
(It might be possible to distinguish because Divisional Courts are held by  two people, one of
whom is very senior)

There are two different types of Family Court, one far more senior than the other.

Whilst we use Neutral Citations heavily in the current version of the Find Caselaw service (most
notably in the URL structure which rearranges the parts, but also currently for search-by-court
purposes, although functionality exists for searching via the value of the `uk:court` tag),
there is a desire that we should be able to reference the courts in a way
that does not rely upon something (Neutral Citations) that does not directly correlate to the Courts
as they exist in reality and that we cannot change.

[A list](https://github.com/nationalarchives/ds-caselaw-data-enrichment-service/blob/665520c2cdc0a69a90804bc83c35adaf8603f7f0/utils/2022_11_04_Court_Mapping.csv)
(pinned to a specific commit) has been made to provide mappings between these concepts,
primarily for the purposes of the ontology and enrichment, and modifies some of the values that
are currently used for the `uk:court` identifier to shorten them and remove dependence on QB/KB distinctions.
(These values have typically been referred to as "Court UIDs")

The currently-proposed "Court UIDs" preserve the arbitary distinctions in Costs/SCCO and QB/KB,
with different Court UIDs for the two different neutral citations. Not having this behaviour would be technically
challenging because "the rules engine requires a one-to-one mapping between [a court's] ID and the
canonical form of the citation."
[[ref]](https://dxw.slack.com/archives/C044HLACKGT/p1668530087239629?thread_ts=1668508243.883489&cid=C044HLACKGT)

(Since a UID typically has a 1:1 mapping with a thing, the name may be imprecise.)

## Decision

Jim, Dragon and Heather discussed this on 16 Nov 2022 and decided that whilst the situation was not ideal,
it is best to continue with this approach of single courts with multiple Court UIDs that refer to them to ensure
the enrichment engine work is not held back. By having multiple Court UIDs per court (but not having Court UIDs
which are shared between multiple courts), we can consider treating the IDs
as interchangable later, or actually changing all references to one `uk:court`-style ID to another, or using
semantic terms to identify that they are the same.

The Divisional Court sharing a Neutral Citation -- and hence a Court UID -- with the Administrative Court
means we will not be able to separate out these two courts easily later, but in practice the Divisional
Court will not initially be used and all such judgments will considered as being from the Administrative Court.

We do not understand enough about the Family Court problems, so we shall ignore them for now

## Consequences

* Clarity on approach for enrichment in the short-term
* Pushing thorny problems down the road until there's more clarity in the use-cases for Court UID identifiers
* We will need to listen to feedback about how our model impacts people's ability to find judgments
