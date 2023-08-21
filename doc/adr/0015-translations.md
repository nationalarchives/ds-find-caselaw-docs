# 15. Translations

Date: 2023-08-15

## Status

Accepted

## Context

We currently use django translations, and find the overhead onerous. We might also be misusing it, where the
recommended approach is to write the text in a human language (`Publish` rather than `document.publish_button_text`)
and then translate to another, with options for providing further context clues to the translation software.

Whilst we anticipate we might want to translate the website into Welsh at some point, it is not a part of our current
roadmap, and we have not properly investigated what it would take to provide Welsh-language content or Welsh-language interface.
We expect there will be a lot of work to do and any work we do now is not guaranteed to support future work. 

## Decision

We will not routinely use translations for new work, unless there is a compelling reward in the short term.
It is mildly encouraged to remove translations and replace them with the corresponding English text from the translation file;
especially where that makes things easier for us.

We should re-evaluate this decision should Welsh language support be added to the roadmap.

## Consequences

This should hopefully make writing templates in one language significantly easier in the short term, whilst not significantly
increasing costs for adding an additional language later.
