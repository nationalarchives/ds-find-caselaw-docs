xquery version "1.0-ml";

module namespace helper = "https://caselaw.nationalarchives.gov.uk/helper";

import module namespace ml = "http://marklogic.com/appservices/search" at "/MarkLogic/appservices/search/search.xqy";

declare namespace akn = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
declare namespace uk = "https://caselaw.nationalarchives.gov.uk";

declare private function remove-quotes($s as xs:string) as xs:string {
    fn:translate($s, '"', '')
};

declare private function make-name-query($q as xs:string) as cts:query {
    let $element as xs:QName := fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'FRBRname')
    let $attribute as xs:QName := fn:QName('', 'value')
    let $options as xs:string* := ()
    let $weight as xs:double := 32.0
    return cts:and-query((
        for $phrase at $pos in fn:tokenize($q, '"')
            let $inside-quotes as xs:boolean := $pos mod 2 eq 0
            return if ($inside-quotes) then
                cts:element-attribute-word-query($element, $attribute, $phrase, $options, $weight)
            else for $word in fn:tokenize(fn:normalize-space($phrase), '\s')
                return cts:element-attribute-word-query($element, $attribute, $word, $options, $weight)
    ))
};

declare private function make-cite-query($q as xs:string) as cts:query {
    let $phrase as xs:string := remove-quotes($q)
    let $element as xs:QName := fn:QName('https://caselaw.nationalarchives.gov.uk/akn', 'cite')
    let $options as xs:string* := ( 'case-insensitive' )
    let $weight as xs:double := 32.0
    return cts:element-word-query($element, $phrase, $options, $weight)
};

declare function make-court-query($court as xs:string) as cts:query {
    let $element as xs:QName := fn:QName('https://caselaw.nationalarchives.gov.uk/akn', 'court')
    let $options as xs:string* := ( 'case-insensitive' )
    return cts:element-value-query($element, $court, $options)
};

declare private function make-phrase-query($q as xs:string) as cts:query? {
    if (fn:contains($q, '"')) then
        ()
    else
        let $phrase as xs:string := remove-quotes($q)
        return cts:word-query($phrase, (), 16.0)
};

declare private function make-simple-q-query($q as xs:string) as cts:query {
    cts:and-query((
        for $phrase at $pos in fn:tokenize($q, '"')
            let $inside-quotes as xs:boolean := $pos mod 2 eq 0
            return
                if ($inside-quotes) then
                    cts:word-query($phrase)
                else
                    let $words as xs:string* := fn:tokenize(fn:normalize-space($phrase), '\s')
                    return (
                        for $word in $words
                            return cts:word-query($word),
                        if (fn:exists($words)) then cts:word-query($words, 'distance-weight=16') else ()
                    )
    ))
};

declare function make-q-query($q as xs:string) as cts:query {
     cts:or-query((
        make-name-query($q),
        make-cite-query($q),
        make-phrase-query($q),
        make-simple-q-query($q)
     ))
};

declare function make-party-query($party as xs:string?) as cts:query? {
    if ($party) then cts:or-query((
        cts:element-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'party'), $party),
        cts:element-attribute-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'FRBRname'), fn:QName('', 'value'), $party)
    )) else ()
};

declare variable $transform-results :=
    <transform-results xmlns="http://marklogic.com/appservices/search" apply="snippet" ns="https://caselaw.nationalarchives.gov.uk/helper" at="/helper.xqy">
        <preferred-matches>
            <element name="p" ns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"/>
        </preferred-matches>
    </transform-results>;

declare function snippet($result as node(), $query as schema-element(cts:query), $options as element(ml:transform-results)?) as element(ml:snippet) {
    let $unfiltered := ml:snippet($result, $query, $options)
    return xdmp:xslt-eval($snippet-filter, $unfiltered)/*
};

declare private variable $snippet-filter := <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0" xmlns:search="http://marklogic.com/appservices/search">
    <xsl:template match="search:match">
        <xsl:choose>
            <xsl:when test="empty(child::node())" />
            <xsl:when test="ends-with(@path, 'court')" />
            <xsl:when test="ends-with(@path, 'year')" />
            <xsl:when test="ends-with(@path, 'number')" />
            <xsl:when test="ends-with(@path, 'cite') and exists(following-sibling::*)" />
            <xsl:otherwise>
                <xsl:next-match />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>;
