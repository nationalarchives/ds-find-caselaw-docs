# ruff: noqa: T201

# """Make a bash script to copy the files across to S3"""

import csv
import re
from collections import Counter
from pathlib import Path
from typing import namedtuple

SOURCE_REPO = "bailii-docx"
TARGET_REPO = "tna-caselaw-unpublished-assets"
DRY_RUN = "--dryrun"
DALMATIAN_INFRASTRUCTURE = "caselaw"

SPREADSHEET = "bailii_files.csv"

# NOTE THIS MUST BE RUN AS A V2 DALMATIAN


class UnexpectedExtension(Exception):
    pass


with Path.open(SPREADSHEET) as f:
    csv_reader = csv.reader(f)
    raw_data = list(csv_reader)

headers = raw_data[0]

Row = namedtuple("Row", headers)
columns = {}
for header in headers:
    columns[header] = Counter()

nice_data = []
for row in raw_data[1:]:
    row_object = Row(**dict(zip(headers, row)))
    nice_data.append(row_object)
    for header in headers:
        columns[header][row_object._asdict()[header]] += 1

for x in columns:
    print(x, columns[x].most_common(10))


def clean_rows(nice_data):
    print(len(nice_data))
    nice_data = [doc for doc in nice_data if doc.tna_id]
    print(len(nice_data), "have tna_id")
    nice_data = [doc for doc in nice_data if doc.deleted == "0"]
    print(len(nice_data), "not deleted")
    nice_data = [doc for doc in nice_data if doc.main == "1"]
    print(len(nice_data), "main")
    # There is one that didn't have a docx, but pdf/UKFTT-TC/2018/TC06353.docx exist just fine
    # print ([doc for doc in nice_data if doc.docx == "0"])
    # nice_data = [doc for doc in nice_data if doc.docx == "1"]
    # print (len(nice_data), "docx")
    # bad_internal_cite is not a reason to not write docx -- we rewrite the path anyway
    # nice_data = [doc for doc in nice_data if doc.bad_internal_cite == "0"]
    # print (len(nice_data), "valid_cite")
    nice_data = [doc for doc in nice_data if doc.xml == "1"]
    print(len(nice_data), "xml")
    nice_data = [doc for doc in nice_data if doc.website == "1"]
    print(len(nice_data), "website")
    return nice_data


def source_key(doc):
    extension_match = re.search(r"^(.*)\.([a-z]*)$", doc.filename)
    root, extension = extension_match.groups()
    if extension not in ["rtf", "pdf", "doc", "docx"]:
        raise UnexpectedExtension
    return f"{extension}/{root}.docx"


def target_key(doc):
    path = doc.tna_id
    filename = doc.tna_id.replace("/", "_") + ".docx"
    return f"{path}/{filename}"


nice_data = clean_rows(nice_data)
print(len(nice_data))

for doc in nice_data:
    print(source_key(doc), target_key(doc))
    print(
        f"dalmatian aws-sso run-command -i {DALMATIAN_INFRASTRUCTURE} -e staging s3 cp 's3://{SOURCE_REPO}/{source_key(doc)}' 's3://{TARGET_REPO}/{target_key(doc)}' {DRY_RUN}",
    )
    # curl https://assets.caselaw.nationalarchives.gov.uk/uksc/2024/1/uksc_2024_1.docx --head -f
