xquery version '1.0-ml';

import module namespace dls = "http://marklogic.com/xdmp/dls" at "/MarkLogic/dls.xqy";

declare variable $URI as xs:string external;

if
  (fn:not(dls:document-is-managed($URI)))
then
  dls:document-manage($URI, fn:true())
else
  fn:false()
