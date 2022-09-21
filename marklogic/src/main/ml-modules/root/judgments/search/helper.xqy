xquery version "1.0-ml";

module namespace helper = "https://caselaw.nationalarchives.gov.uk/helper";

import module namespace ml = "http://marklogic.com/appservices/search" at "/MarkLogic/appservices/search/search.xqy";

declare namespace akn = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0";
declare namespace uk = "https://caselaw.nationalarchives.gov.uk";

declare variable $default-options as xs:string* := ( 'case-insensitive' );

declare private function make-simple-name-query($word as xs:string) as cts:query {
    let $element as xs:QName := fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'FRBRname')
    let $attribute as xs:QName := fn:QName('', 'value')
    let $options as xs:string* := $default-options
    let $weight as xs:double := 16.0
    return cts:element-attribute-word-query($element, $attribute, $word, $options, $weight)
};

declare private function make-simple-cite-query($phrase as xs:string) as cts:query {
    let $element as xs:QName := fn:QName('https://caselaw.nationalarchives.gov.uk/akn', 'cite')
    let $options as xs:string* := ( 'case-insensitive' )
    let $weight as xs:double := 32.0
    return cts:element-word-query($element, $phrase, $options, $weight)
};

declare private function make-simple-party-query($phrase as xs:string) as cts:query {
    let $element as xs:QName := fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'party')
    let $options as xs:string* := $default-options
    let $weight as xs:double := 8.0
    return cts:element-word-query($element, $phrase, $options, $weight)
};

declare private function make-simple-body-query($phrase as xs:string, $weight as xs:double) as cts:word-query {
    cts:word-query($phrase, $default-options, $weight)
};
declare private function make-simple-body-query($phrase as xs:string) as cts:word-query {
    make-simple-body-query($phrase, 1.0)
};

declare private function make-name-party-or-body-query($phrase as xs:string, $weight as xs:double) as cts:or-query {
    cts:or-query((
        make-simple-name-query($phrase),
        make-simple-party-query($phrase),
        make-simple-body-query($phrase, $weight)
    ))
};
declare private function make-name-party-or-body-query($phrase as xs:string) as cts:or-query {
    make-name-party-or-body-query($phrase, 1.0)
};
declare private function make-name-party-or-body-queries($phrase as xs:string) as cts:query {
    let $words as xs:string+ := fn:tokenize($phrase, '\s') (: $phrase is normalized and not empty :)
    let $phrase-weight as xs:double := 4.0
    let $distance-weight as xs:string := 'distance-weight=2'
    return
        if (fn:empty(fn:tail($words))) then
            make-name-party-or-body-query($phrase)
        else
            cts:or-query((
                cts:and-query((
                    for $word in $words
                    return make-name-party-or-body-query($word),
                    cts:word-query($words, ($default-options, $distance-weight))
                )),
                make-simple-body-query($phrase, $phrase-weight)
            ))
};

declare private function make-cite-or-body-query($phrase as xs:string) as cts:or-query {
    cts:or-query((
        make-simple-cite-query($phrase),
        make-simple-body-query($phrase, 2.0)
    ))
};

declare function make-court-query($court as xs:string) as cts:query {
    let $element as xs:QName := fn:QName('https://caselaw.nationalarchives.gov.uk/akn', 'court')
    let $options as xs:string* := ( 'case-insensitive' )
    return cts:element-value-query($element, $court, $options)
};

declare private function is-a-neutral-citation-2($phrase as xs:string, $patterns as xs:string*) as xs:boolean {
    if (fn:empty($patterns)) then
        false()
    else
        fn:matches($phrase, fn:head($patterns), 'i') or is-a-neutral-citation-2($phrase, fn:tail($patterns))
};

declare private function match-neutral-citation-2($phrase as xs:string, $patterns as xs:string*) as element(fn:analyze-string-result)? {
    if (fn:empty($patterns)) then
        ()
    else
        let $match := fn:analyze-string($phrase, fn:head($patterns), 'i')
        return
            if (fn:exists($match/fn:match)) then
                $match
            else
                match-neutral-citation-2($phrase, fn:tail($patterns))
};

declare private variable $neutral-citation-patterns as xs:string+ := (
    '(^| )\[?\d{4}\]? (UKSC|UKPC) \d+( |$)',
        '(^| )\[?\d{4}\]? (UKSC|UKPC)( |$)',
        '(^| )(UKSC|UKPC) \d+( |$)',
    '(^| )\[?\d{4}\]? EWCA (Civ|Crim) \d+( |$)',
        '(^| )\[?\d{4}\]? EWCA (Civ|Crim)( |$)',
        '(^| )\[?\d{4}\]? EWCA( |$)',
        '(^| )EWCA (Civ|Crim) \d+( |$)',
        '(^| )EWCA (Civ|Crim)( |$)',
        '(^| )(Civ|Crim) \d+( |$)',
    '(^| )\[?\d{4}\]? EWHC \d+ \(?(Admin|Admlty|Ch|Comm|Costs|Fam|IPEC|Pat|QB|KB|TCC)\)?( |$)',
        '(^| )\[?\d{4}\]? EWHC \d+( |$)',
        '(^| )\[?\d{4}\]? EWHC( |$)',
        '(^| )EWHC \d+ \(?(Admin|Admlty|Ch|Comm|Costs|Fam|IPEC|Pat|QB|KB|TCC)\)?( |$)',
        '(^| )EWHC \d+( |$)',
        (: '(^| )\d+ \(?(Admin|Admlty|Ch|Comm|Costs|Fam|IPEC|Pat|QB|KB|TCC)\)?( |$)', :)
    '(^| )\[?\d{4}\]? (EWFC|EWCOP) \d+( |$)',
        '(^| )\[?\d{4}\]? (EWFC|EWCOP)( |$)',
        '(^| )(EWFC|EWCOP) \d+( |$)',
    '(^| )\[?\d{4}\]? UKUT \d+ \(?(AAC|IAC|LC|TCC)\)?( |$)',
        '(^| )\[?\d{4}\]? UKUT \d+( |$)',
        '(^| )\[?\d{4}\]? UKUT( |$)',
        '(^| )UKUT \d+ \(?(AAC|IAC|LC|TCC)\)?( |$)',
        '(^| )UKUT \d+( |$)',
        (: '(^| )\d+ \(?(AAC|IAC|LC|TCC)\)?( |$)', :)
    '(^| )\[?\d{4}\]? EAT \d+( |$)',
        '(^| )\[?\d{4}\]? EAT( |$)',
        '(^| )EAT \d+( |$)',
    '(^| )\[?\d{4}\]? UKFTT \d+ \(?(TC)\)?( |$)',
        '(^| )\[?\d{4}\]? UKFTT \d+( |$)',
        '(^| )\[?\d{4}\]? UKFTT( |$)',
        '(^| )UKFTT \d+ \(?(TC)\)?( |$)',
        '(^| )UKFTT \d+( |$)'
        (: '(^| )\d+ \(?(TC)\)?( |$)' :)
);

declare private function is-a-neutral-citation($phrase as xs:string) as xs:boolean {
    is-a-neutral-citation-2($phrase, $neutral-citation-patterns)
};

declare private function match-neutral-citation($phrase as xs:string) as element(fn:analyze-string-result)? {
    match-neutral-citation-2($phrase, $neutral-citation-patterns)
};

declare private variable $consignment-number-pattern as xs:string := '^TDR-\d{4}-.+';

declare function is-a-consignment-number($phrase as xs:string) as xs:boolean {
    if (fn:empty($phrase)) then
        false()
    else
        fn:matches($phrase, $consignment-number-pattern, 'i')
};

declare function make-consignment-number-query($consignment-number as xs:string) {
    cts:properties-fragment-query(
        cts:element-value-query(
            fn:QName("", "transfer-consignment-reference"),
            $consignment-number,
            ("case-insensitive")
        )
    )
};

declare function make-q-query($q as xs:string) {
    let $q := fn:replace($q, '- *v *-', ' v ', 'i')
    let $q := fn:normalize-space($q)
    return cts:and-query((
        for $phrase at $pos in fn:tokenize($q, '"')
        let $phrase := fn:normalize-space($phrase)
        let $inside-quotes as xs:boolean := $pos mod 2 eq 0
        where $phrase
        return
            if ($inside-quotes) then
                if (is-a-neutral-citation($phrase)) then
                    make-cite-or-body-query($phrase)
                else
                    make-name-party-or-body-query($phrase, 4.0)
            else
                let $result as element(fn:analyze-string-result)? := match-neutral-citation($phrase)
                return
                    if (fn:empty($result)) then (: not a neutral citation :)
                        make-name-party-or-body-queries($phrase)
                    else
                        for $child in $result/*
                        let $normalized as xs:string := fn:normalize-space($child)
                        where $normalized
                        return
                            if ($child/self::fn:match) then
                                make-cite-or-body-query($normalized)
                            else
                                make-name-party-or-body-queries($normalized)
    ))
};

declare function make-party-query($party as xs:string?) as cts:query? {
    let $weight as xs:double := 8.0
    return
        if ($party) then
            cts:or-query((
                cts:element-attribute-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'FRBRname'), fn:QName('', 'value'), $party, $default-options, $weight * 2),
                cts:element-word-query(fn:QName('http://docs.oasis-open.org/legaldocml/ns/akn/3.0', 'party'), $party, $default-options, $weight)
            ))
        else
            ()
};

declare variable $transform-results :=
    <transform-results xmlns="http://marklogic.com/appservices/search" apply="snippet" ns="https://caselaw.nationalarchives.gov.uk/helper" at="/judgments/search/helper.xqy">
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
