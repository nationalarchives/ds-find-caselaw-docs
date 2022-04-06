xquery version "1.0-ml";

let $uris := cts:uris()
return (fn:count($uris), $uris)
