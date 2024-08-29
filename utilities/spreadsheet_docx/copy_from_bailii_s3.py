# ruff: noqa: T201 (print)
# ruff: noqa: S603 (untrusted subprocess input)
# ruff: noqa: PYI024 (typing.NamedTuple instead of collections)


# """Make a bash script to copy the files across to S3"""

import csv
import json
import re
import subprocess
import sys
from collections import Counter, namedtuple
from pathlib import Path

import requests

SOURCE_BUCKET = "bailii-docx"
UNPUBLISHED_BUCKET = "tna-caselaw-unpublished-assets"
PUBLISHED_BUCKET = "tna-caselaw-assets"
DALMATIAN_INFRASTRUCTURE = "caselaw"
ASSETS_BASE = "https://tna-caselaw-assets.s3.amazonaws.com"
CASELAW_BASE = "https://caselaw.nationalarchives.gov.uk"

SPREADSHEET = "bailii_files.csv"
DRY_RUN = "--for-real" not in sys.argv[1:]
if not DRY_RUN:
    print("Running for real...")

# NOTE THIS MUST BE RUN AS A V2 DALMATIAN
# Run `dalmatian version -v 2` first


class UnexpectedExtension(Exception):
    pass


with Path(SPREADSHEET).open() as f:
    csv_reader = csv.reader(f)
    raw_data = list(csv_reader)

headers = raw_data[0]

BaseRow = namedtuple("Row", headers)


class Row(BaseRow):
    def source_key(self):
        extension_match = re.search(r"^(.*)\.([a-z]*)$", self.filename)
        root, extension = extension_match.groups()
        if extension not in ["rtf", "pdf", "doc", "docx"]:
            raise UnexpectedExtension
        return f"{extension}/{root}.docx"

    def target_key(self):
        path = self.tna_id
        filename = self.tna_id.replace("/", "_") + ".docx"
        return f"{path}/{filename}"

    def has_docx_in_s3(self):
        response = requests.head(f"{ASSETS_BASE}/{self.target_key()}", timeout=30)
        return response.status_code == 200

    def is_published(self):
        response = requests.head(f"{CASELAW_BASE}/{self.tna_id}", timeout=30)
        return response.status_code == 200

    def copy_command(self, target_bucket):
        if target_bucket == UNPUBLISHED_BUCKET:
            public_bonus = []
        elif target_bucket == PUBLISHED_BUCKET:
            public_bonus = [
                "--acl",
                "public-read",
            ]
        else:
            raise RuntimeError

        dryrun_bonus = ["--dryrun"] if DRY_RUN else []

        command = [
            "dalmatian",
            "aws-sso",
            "run-command",
            "-i",
            DALMATIAN_INFRASTRUCTURE,
            "-e",
            "staging",
            "s3",
            "cp",
            f"s3://{SOURCE_BUCKET}/{doc.source_key()}",
            f"s3://{target_bucket}/{doc.target_key()}",
            "--copy-props",
            "none",
            "--acl",
            "bucket-owner-full-control",
        ]

        command.extend(public_bonus)
        command.extend(dryrun_bonus)
        return command


columns = {}
for header in headers:
    columns[header] = Counter()

nice_data = []
for row in raw_data[1:]:
    row_object = Row(**dict(zip(headers, row)))
    if len(row) != len(headers):
        msg = "Data not rectangular"
        raise RuntimeError(msg)
    nice_data.append(row_object)
    for header in headers:
        columns[header][row_object._asdict()[header]] += 1

for x in columns:
    print(x, columns[x].most_common(10))


def clean_rows(nice_data):
    """drop data that doesn't have tna id's etc, report on number left"""
    print(len(nice_data))
    nice_data = [doc for doc in nice_data if doc.tna_id]
    print(len(nice_data), "have tna_id")
    nice_data = [doc for doc in nice_data if doc.deleted == "0"]
    print(len(nice_data), "not deleted")
    nice_data = [doc for doc in nice_data if doc.main == "1"]
    print(len(nice_data), "main")
    # There is one that didn't have a docx, but pdf/UKFTT-TC/2018/TC06353.docx exists just fine
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


nice_data = clean_rows(nice_data)
print(len(nice_data))

for row_num, doc in enumerate(nice_data):

    if row_num < 33959:
        continue
    
    if doc.has_docx_in_s3():
        print(f"Skipping #{row_num} {doc.target_key()}, exists")
        continue

    print(f"Writing #{row_num} {doc.source_key()} to {doc.target_key()}...")

    command = doc.copy_command(UNPUBLISHED_BUCKET)
    print(command)
    retcode = subprocess.run(command, check=False).returncode

    if retcode != 0:
        raise RuntimeError

    if not doc.is_published():
        print(f"Skipping public upload of {doc.target_key()}, not published")
        with Path("not_published.jsonl").open("a") as f:
            f.write(json.dumps([doc.source_key(), doc.target_key()]) + "\n")
        continue

    command = doc.copy_command(PUBLISHED_BUCKET)
    print(command)
    retcode = subprocess.run(command, check=False).returncode

    if retcode != 0:
        raise RuntimeError
