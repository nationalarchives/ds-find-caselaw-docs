# ruff: noqa: T201
import re
import sys
from pathlib import Path
from typing import NamedTuple

unpub_prefix = "https://eu-west-2.console.aws.amazon.com/s3/object/tna-caselaw-unpublished-assets?region=eu-west-2&bucketType=general&prefix="
pub_prefix = "https://assets.caselaw.nationalarchives.gov.uk/"


def link(url, text):
    if sys.stdout.isatty():
        return f"\u001b]8;;{url}\u001b\\{text}\u001b]8;;\u001b\\"
    return text


Entry = NamedTuple("Entry", ["date", "time", "size", "name"])


class ParsedLS:
    def __init__(self, listing):
        self.listing = listing
        with Path.open(listing) as f:
            self.rawdata = f.readlines()
        self.data = []
        for item in self.rawdata:
            parsed_row = re.findall(r"(....-..-..) (..:..:..) *(\d+) (.*)", item)
            date, time, size, name = parsed_row[0]
            self.data.append(Entry(date, time, size, name))

    def as_name_dict(self):
        return {item.name: item for item in self.data}


pub = ParsedLS("pub.txt")
unpub = ParsedLS("unpub.txt")

pub_dict = pub.as_name_dict()
unpub_dict = unpub.as_name_dict()

for name, pub_item in pub_dict.items():
    if name not in unpub_dict:
        print(f"{name} not in unpub")
    else:
        pub_size = pub_item.size
        unpub_size = unpub_dict[name].size
        if pub_size != unpub_size:
            print(
                f"{name} is {pub_size} in {link(pub_prefix+name, "published bucket")} but {unpub_size} in {link(unpub_prefix+name, "unpublished")}",
            )
