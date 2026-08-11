xquery version "1.0-ml";

declare namespace uk = "https://caselaw.nationalarchives.gov.uk/akn";

(: 1. Loop through the first 100 matching URIs :)
for $uri in cts:uris(
  "",
  "limit=100",
  cts:and-query((
    cts:collection-query("http://marklogic.com/collections/dls/latest-version"),
    cts:not-query(
      cts:collection-query("press-summary")
    ),
    cts:not-query(
      cts:collection-query("parser-log")
    ),
    cts:not-query(
      cts:properties-fragment-query(
        cts:element-value-query(xs:QName("namespace"), "ukncn")
      )
    ),
    cts:not-query(
      cts:element-query(xs:QName("uk:party"), cts:true-query())
    )
  ))
)

(: 2. Fetch the main document and the properties fragment for the current URI :)
let $doc := fn:doc($uri)
let $props := xdmp:document-properties($uri)

(: 3. Extract the court value :)
let $court := $doc//uk:court/fn:string()

(: 4. Locate the url_slug specifically within the fclid identifier block :)
let $fclid-slug := $props//identifier[namespace = "fclid"]/url_slug/fn:string()

(: 5. Construct the URL (with a fallback just in case an fclid isn't present) :)
let $url :=
  if ($fclid-slug)
  then fn:concat("https://caselaw.nationalarchives.gov.uk/", $fclid-slug)
  else "No fclid slug found"

(: 6. Return the constructed data as a JSON object :)
return
  object-node {
    "uri": $uri,
    "court": $court,
    "url": $url
  }
