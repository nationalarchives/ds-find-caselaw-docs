xquery version "1.0-ml";

import module namespace search = "http://marklogic.com/appservices/search" at "/MarkLogic/appservices/search/search.xqy";
import module namespace helper = "https://caselaw.nationalarchives.gov.uk/helper" at "./helper.xqy";
import module namespace dls = "http://marklogic.com/xdmp/dls" at "/MarkLogic/dls.xqy";
import module namespace cpf = "http://marklogic.com/cpf" at "/MarkLogic/cpf/cpf.xqy";

declare namespace akn = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
declare namespace uk = "https://caselaw.nationalarchives.gov.uk";

declare function uk:get-request-date($name as xs:string) as xs:date? {
    let $raw := $name
    return if ($raw castable as xs:date) then xs:date($raw) else ()
};

declare variable $q as xs:string? external;
declare variable $party as xs:string? external;
declare variable $court as json:array? external;
declare variable $judge as xs:string? external;
declare variable $neutral_citation as xs:string? external;
declare variable $specific_keyword as xs:string? external;
declare variable $order as xs:string? external;
declare variable $page as xs:integer external;
declare variable $page-size as xs:integer external;
declare variable $from as xs:string? external;
declare variable $to as xs:string? external;
declare variable $from_date as xs:date? := uk:get-request-date($from);
declare variable $to_date as xs:date? := uk:get-request-date($to);
declare variable $show_unpublished as xs:boolean? external;
declare variable $only_unpublished as xs:boolean? external;

let $start as xs:integer := ($page - 1) * $page-size + 1

let $params := map:map()
    => map:with('q', $q)
    => map:with('party', $party)
    => map:with('court', $court)
    => map:with('judge', $judge)
    => map:with('neutral_citation', $neutral_citation)
    => map:with('specific_keyword', $specific_keyword)
    => map:with('page', $page)
    => map:with('page-size', $page-size)
    => map:with('order', $order)
    => map:with('from', $from)
    => map:with('to', $to)
    => map:with('show_unpublished', $show_unpublished)
    => map:with('only_unpublished', $only_unpublished)

let $query1 := if ($q) then helper:make-q-query($q) else ()
let $query2 := if ($party) then
    cts:or-query((
        cts:element-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'party'), $party),
        cts:element-attribute-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'FRBRname'), fn:QName('', 'value'), $party)
    ))
else ()

let $query4 := if ($court) then cts:or-query(
    for $c in json:array-values($court) return (
    cts:element-value-query(fn:QName('https://judgments.gov.uk/', 'court'), $c, ('case-insensitive')),
    cts:element-value-query(fn:QName('https://caselaw.nationalarchives.gov.uk/akn', 'court'), $c, ('case-insensitive')),
    cts:element-attribute-word-query(
    fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'FRBRuri'), xs:QName('value'), $c, ('case-insensitive')
    )
)) else ()


let $query5 := if ($judge) then cts:element-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'judge'), $judge, ('case-insensitive', 'punctuation-insensitive')) else ()
let $query6 := if (empty($from_date)) then () else cts:path-range-query('akn:FRBRWork/akn:FRBRdate/@date', '>=', $from_date)
let $query7 := if (empty($to_date)) then () else cts:path-range-query('akn:FRBRWork/akn:FRBRdate/@date', '<=', $to_date)
let $query8 := if ($show_unpublished or $only_unpublished) then () else cts:properties-fragment-query(cts:element-value-query(fn:QName("", "published"), "true"))
let $query9 := if ($only_unpublished) then cts:properties-fragment-query(cts:not-query(cts:element-value-query(fn:QName("", "published"), "true"))) else ()
let $query10 := if ($neutral_citation) then
    cts:element-value-query(fn:QName('https://caselaw.nationalarchives.gov.uk/akn', 'cite'), $neutral_citation, ('case-insensitive'))
else ()
let $query11 := if ($specific_keyword) then
    cts:word-query($specific_keyword, ('case-insensitive', 'unstemmed'))
else ()
let $query12 := if (helper:is-a-consignment-number($q)) then (helper:make-consignment-number-query($q)) else ()


let $queries := ( $query1, $query2, $query4, $query5, $query6, $query7, $query8, $query9, $query10, $query11, $query12, dls:documents-query() )
let $query := cts:and-query($queries)

let $show-snippets as xs:boolean := exists(( $query1, $query2, $query5 ))

let $sort-order := if ($order = 'date') then
    <sort-order xmlns="http://marklogic.com/appservices/search" direction="ascending">
        <path-index xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">akn:FRBRWork/akn:FRBRdate/@date</path-index>
    </sort-order>
else if ($order = '-date') then
    <sort-order xmlns="http://marklogic.com/appservices/search" direction="descending">
        <path-index xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">akn:FRBRWork/akn:FRBRdate/@date</path-index>
    </sort-order>
else if ($order = '-updated') then
     <sort-order xmlns="http://marklogic.com/appservices/search" direction="descending" type="xs:dateTime">
        <element ns="http://marklogic.com/xdmp/property" name="last-modified" />
    </sort-order>
else if ($order = 'updated') then
    <sort-order xmlns="http://marklogic.com/appservices/search" direction="ascending" type="xs:dateTime">
        <element ns="http://marklogic.com/xdmp/property" name="last-modified" />
    </sort-order>
else if ($order = '-transformation') then
    <sort-order xmlns="http://marklogic.com/appservices/search" direction="ascending">
        <path-index xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">akn:akomaNtoso/akn:judgment/akn:meta/akn:identification/akn:FRBRManifestation/akn:FRBRdate[@name='transform']/@date</path-index>
    </sort-order>
else if ($order = 'transformation') then
    <sort-order xmlns="http://marklogic.com/appservices/search" direction="descending">
        <path-index xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">akn:akomaNtoso/akn:judgment/akn:meta/akn:identification/akn:FRBRManifestation/akn:FRBRdate[@name='transform']/@date</path-index>
    </sort-order>
else
    ()

let $transform-results := if ($show-snippets) then
    $helper:transform-results
else
    <transform-results xmlns="http://marklogic.com/appservices/search" apply="empty-snippet" />


let $scope := if ($order = 'updated') then
    'properties'
else if ($order = '-updated') then
    'properties'
else if (exists($query12)) then
    'properties'
else
    'documents'


let $search-options := <options xmlns="http://marklogic.com/appservices/search">
    <fragment-scope>{ $scope }</fragment-scope>
    <search-option>unfiltered</search-option>
    { $sort-order }
    <extract-document-data xmlns:akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
        <extract-path>//akn:FRBRWork/akn:FRBRdate</extract-path>
        <extract-path>//akn:FRBRWork/akn:FRBRname</extract-path>
        <extract-path>//uk:cite</extract-path>
        <extract-path>//akn:neutralCitation</extract-path>
        <extract-path>//uk:court</extract-path>
        <extract-path>//uk:hash</extract-path>
        <extract-path>//akn:FRBRManifestation/akn:FRBRdate</extract-path>
    </extract-document-data>
    { $transform-results }
</options>

let $results := search:resolve(element x { $query }/*, $search-options, $start, $page-size)
let $total as xs:integer := xs:integer($results/@total)
let $pages as xs:integer := if ($total mod $page-size eq 0) then $total idiv $page-size else $total idiv $page-size + 1
let $params := $params => map:with('pages', $pages)

return $results
