xquery version "1.0-ml";

import module namespace dls = "http://marklogic.com/xdmp/dls" at "/MarkLogic/dls.xqy";

let $uris := cts:uris("", (), dls:documents-query())
return (fn:count($uris), $uris)
