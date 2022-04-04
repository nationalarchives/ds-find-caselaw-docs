xquery version '1.0-ml';

import module namespace trgr = 'http://marklogic.com/xdmp/triggers' at '/MarkLogic/triggers.xqy';
import module namespace dls = "http://marklogic.com/xdmp/dls" at "/MarkLogic/dls.xqy";

declare variable $trgr:uri as xs:string external;

if
  (fn:not(dls:document-is-managed($trgr:uri)))
then
  dls:document-manage($trgr:uri, fn:true())
else
  fn:false()
