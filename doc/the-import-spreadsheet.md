(From discussion at
https://dxw.slack.com/archives/C04FQ3GFGUQ/p1699463646068439
https://dxw.slack.com/archives/C02TP2L2Z0F/p1720540543957149
)

The "back catalogue" spreadsheet contains all the information we had about judgments published before launch.

https://trello.com/1/cards/654bc37c6e509bf4a921c395/attachments/654bc58009e8d4cf622042fd/download/back_cat.xlsx
(from https://trello.com/c/bRvB0uGK)

So, for example, you can tell which documents we received as PDF, etc.

There were three different sources of documents: BAILII, “other” (including the Supreme Court), and what I called “new” (documents received directly from the courts via their email distribution list, before TDR was operational)
https://trello.com/c/Xhl3q3Sa has more info on this.

The “internal” metadata fields show the metadata values the parser had identified. The other metadata tabs show metadata values that I gave to the parser along with the .docx (and which would then trump the others)

1 in “deleted” means ignore it
“main” mean it’s a judgment (0 means it’s an associated document)
“docx” means I was able to generate a .docx from the original
“bad_internal_cite” means the NCN in the document is not correct
“xml” means the parser was able to complete parsing
“website” means it was uploaded it to the prototype MarkLogic (from which the judgments were eventually taken)
filename: original bailii filename
tna_id: our ID

Almost all of the original filenames are good -- there are 13 which do not have the correct original name (see bad_internal_cite).
[We should be able to rewrite the filename of these files using the URL path]
(We are intending to copy files from the bailii-docx bucket to production S3)
We are only intending to handle the bailii_files tab for now

The source and destination filenames will need mangling -- whilst there should only be the best file format in the spreadsheet,
if the source filename is EAT/2000/1.rtf, the transformed docx will be at /rtf/EAT/2000/1.docx.
And if the tna_id filename is eat/2000/1, the target should be eat/2000/1/eat_2000_1.docx
We should ignore all lines with a '0' for tna_id

Theoretically, there might be two files with different extensions: .docx and .doc; .rtf and .pdf etc with the same name
The spreadsheet should have already chosen the docx in preference, but don't overwrite as a precaution.

TODO: check if I have permissions to bailii-docx
TODO: check if no tna-id documents are sensible and should be uploaded -- ewca/civ/2003/496 might be one of them.
