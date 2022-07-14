xquery version "1.0-ml";

import module namespace cdict = "http://marklogic.com/xdmp/custom-dictionary"
  at "/MarkLogic/custom-dictionary.xqy";

let $dict :=
  <cdict:dictionary xmlns:cdict="http://marklogic.com/xdmp/custom-dictionary">
    <cdict:entry>
      <cdict:word>racial</cdict:word>
      <cdict:stem>race</cdict:stem>
    </cdict:entry>
    <cdict:entry>
      <cdict:word>discriminatory</cdict:word>
      <cdict:stem>discrimination</cdict:stem>
    </cdict:entry>
  </cdict:dictionary>
return cdict:dictionary-write("en", $dict)