import json
import sys

import caselawclient.Client
import environ
from requests_toolbelt.multipart import decoder

environ.Env.read_env()

client = caselawclient.Client.api_client
page = 0
page_size = 250
part = True

while part:
    mindoc = 1 + (page_size * page)
    maxdoc = page_size * (page + 1)

    print(f"Page {page}, ({mindoc}-{maxdoc})", file=sys.stderr)
    query_vars = json.dumps({"mindoc": mindoc, "maxdoc": maxdoc})
    response = client.eval(
        xquery_path="my_xquery.xqy",
        vars=query_vars,
        accept_header="application/xml",
    )
    if not response.content:
        break
    multipart_data = decoder.MultipartDecoder.from_response(response)
    print(len(multipart_data.parts), file=sys.stderr)
    for part in multipart_data.parts:
        print(part.text)
    print(part.text, file=sys.stderr)
    page = page + 1
