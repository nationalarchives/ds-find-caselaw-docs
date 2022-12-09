<?xml version="1.0" encoding="utf-8"?>

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	xpath-default-namespace="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
	xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"
	xmlns:html="http://www.w3.org/1999/xhtml"
	xmlns:math="http://www.w3.org/1998/Math/MathML"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="uk html math xs">

<xsl:output method="html" encoding="utf-8" indent="no" include-content-type="no" />

<xsl:strip-space elements="*" />
<xsl:preserve-space elements="p block num heading span a courtType date docDate docTitle docketNumber judge lawyer location neutralCitation party role time" />

<xsl:param name="image-base" as="xs:string" select="'https://judgment-images.s3.eu-west-2.amazonaws.com/'" />

<xsl:function name="uk:link-is-supported" as="xs:boolean">
	<xsl:param name="href" as="attribute()?" />
	<xsl:choose>
		<xsl:when test="starts-with($href, 'https://www.legislation.gov.uk/')">
			<xsl:sequence select="true()" />
		</xsl:when>
		<xsl:when test="starts-with($href, 'https://caselaw.nationalarchives.gov.uk/')">
			<xsl:variable name="components" as="xs:string*" select="tokenize(substring-after($href, 'https://caselaw.nationalarchives.gov.uk/'), '/')" />
			<xsl:choose>
				<xsl:when test="empty($components[3])">
					<xsl:sequence select="false()" />
				</xsl:when>
				<xsl:when test="$components[1] = ('uksc', 'ukpc')">
					<xsl:sequence select="$components[2] ge '2014'" />
				</xsl:when>
				<xsl:when test="$components[1] = ('ewca', 'ewhc')">
					<xsl:sequence select="$components[3] ge '2003'" />
				</xsl:when>
				<xsl:when test="$components[1] = 'ewcop'">
					<xsl:sequence select="$components[2] ge '2009'" />
				</xsl:when>
				<xsl:when test="$components[1] = 'ewfc'">
					<xsl:sequence select="$components[2] ge '2014'" />
				</xsl:when>
				<xsl:when test="$components[1] = 'ukut'">
					<xsl:choose>
						<xsl:when test="$components[2] = 'iac'">
							<xsl:sequence select="$components[3] ge '2010'" />
						</xsl:when>
						<xsl:when test="$components[2] = 'lc'">
							<xsl:sequence select="$components[3] ge '2015'" />
						</xsl:when>
						<xsl:when test="$components[2] = 'tcc'">
							<xsl:sequence select="$components[3] ge '2017'" />
						</xsl:when>
						<xsl:otherwise>
							<xsl:sequence select="false()" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:sequence select="false()" />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:otherwise>
			<xsl:sequence select="false()" />
		</xsl:otherwise>
	</xsl:choose>
</xsl:function>

<xsl:variable name="doc-id" as="xs:string">
	<xsl:variable name="work-uri" as="xs:string">
		<xsl:sequence select="/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRthis/@value" />
	</xsl:variable>
	<xsl:variable name="long-form-prefix" as="xs:string" select="'https://caselaw.nationalarchives.gov.uk/id/'" />
	<xsl:choose>
		<xsl:when test="starts-with($work-uri, $long-form-prefix)">
			<xsl:sequence select="substring-after($work-uri, $long-form-prefix)" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:sequence select="$work-uri" />
		</xsl:otherwise>
	</xsl:choose>
</xsl:variable>

<xsl:template match="meta" />

<xsl:template match="judgment">
	<article class="judgment">
		<xsl:apply-templates />
		<xsl:apply-templates select="attachments/attachment/doc[@name=('annex','schedule')]" />
		<xsl:call-template name="footnotes">
			<xsl:with-param name="footnotes" as="element()*">
				<xsl:sequence select="header//authorialNote" />
				<xsl:sequence select="judgmentBody//authorialNote" />
				<xsl:sequence select="attachments/attachment/doc[@name=('annex','schedule')]//authorialNote" />
			</xsl:with-param>
		</xsl:call-template>
		<xsl:apply-templates select="attachments/attachment/doc[not(@name=('annex','schedule'))]" />
	</article>
</xsl:template>

<xsl:template match="attachments" />

<xsl:template match="coverPage | header">
	<header class="judgment-header">
		<xsl:apply-templates />
	</header>
</xsl:template>

<xsl:template match="judgmentBody">
	<section class="judgment-body">
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[@name=('annex','schedule')]">
	<section>
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[not(@name=('annex','schedule'))]">
	<section>
		<xsl:apply-templates />
		<xsl:call-template name="footnotes" />
	</section>
</xsl:template>

<xsl:template match="doc[not(@name=('annex','schedule'))]/mainBody">
	<div>
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="decision">
	<xsl:choose>
		<xsl:when test="exists(preceding-sibling::*) or exists(following-sibling::*)">
			<section>
				<xsl:apply-templates />
			</section>
		</xsl:when>
		<xsl:otherwise>
			<xsl:next-match />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="level">
	<section>
		<xsl:if test="num | heading">
			<p>
				<xsl:apply-templates select="num | heading" />
			</p>
		</xsl:if>
		<xsl:apply-templates select="* except (num, heading)" />
	</section>
</xsl:template>

<xsl:template match="paragraph">
	<section class="judgment-body__section">
		<xsl:apply-templates select="@eId" />
		<span class="judgment-body__number">
			<xsl:apply-templates select="num/node()" />
		</span>
		<div>
			<xsl:apply-templates select="* except num" />
		</div>
	</section>
</xsl:template>

<xsl:template match="paragraph/@eId">
	<xsl:attribute name="id">
		<xsl:sequence select="." />
	</xsl:attribute>
</xsl:template>

<xsl:template match="subparagraph">
	<section class="judgment-body__nested-section">
		<span class="judgment-body__number">
			<xsl:apply-templates select="num/node()" />
		</span>
		<div>
			<xsl:apply-templates select="* except num" />
		</div>
	</section>
</xsl:template>

<xsl:template match="paragraph/*/p | subparagraph/*/p">
	<p>
		<xsl:attribute name="class">
			<xsl:choose>
				<xsl:when test="position() = 1">judgment-body__text judgment-body__no-margin-top</xsl:when>
				<xsl:otherwise>judgment-body__text</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
		<xsl:apply-templates>
			<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
		</xsl:apply-templates>
	</p>
</xsl:template>

<!-- <xsl:template match="hcontainer[@name='tableOfContents']" /> -->

<xsl:template match="blockContainer[exists(p)]">
	<xsl:apply-templates select="* except num" />
</xsl:template>

<xsl:template match="blockContainer">
	<xsl:apply-templates />
</xsl:template>

<xsl:template match="blockContainer/num">
	<span>
		<xsl:call-template name="inline" />
	</span>
</xsl:template>

<xsl:template match="blockContainer/p[1]">
	<p>
		<xsl:if test="exists(ancestor::header)">
			<xsl:variable name="alignment" as="xs:string?" select="uk:extract-alignment(.)" />
			<xsl:if test="$alignment = ('center', 'right', 'left')">
				<xsl:attribute name="class">
					<xsl:sequence select="concat('judgment-header__pr-', $alignment)" />
				</xsl:attribute>
			</xsl:if>
		</xsl:if>
		<xsl:apply-templates select="../num" />
		<xsl:text> </xsl:text>
		<span>
			<xsl:apply-templates>
				<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
			</xsl:apply-templates>
		</span>
	</p>
</xsl:template>

<xsl:template match="blockContainer/p[position() gt 1]">
	<p>
		<xsl:if test="exists(ancestor::header)">
			<xsl:variable name="alignment" as="xs:string?" select="uk:extract-alignment(.)" />
			<xsl:if test="$alignment = ('center', 'right', 'left')">
				<xsl:attribute name="class">
					<xsl:sequence select="concat('judgment-header__pr-', $alignment)" />
				</xsl:attribute>
			</xsl:if>
		</xsl:if>
		<xsl:apply-templates>
			<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
		</xsl:apply-templates>
	</p>
</xsl:template>

<xsl:variable name="global-styles" as="xs:string" select="normalize-space(string(/akomaNtoso/judgment/meta/presentation))" />

<xsl:function name="uk:extract-alignment" as="xs:string?">
	<xsl:param name="p" as="element()" />
	<xsl:variable name="from-style-attr" as="xs:string?">
		<xsl:if test="exists($p/@style)">
			<xsl:analyze-string select="$p/@style" regex="text-align: *([a-z]+)">
				<xsl:matching-substring>
					<xsl:sequence select="regex-group(1)"/>
				</xsl:matching-substring>
			</xsl:analyze-string>
		</xsl:if>
	</xsl:variable>
	<xsl:choose>
		<xsl:when test="exists($from-style-attr)">
			<xsl:sequence select="$from-style-attr" />
		</xsl:when>
		<xsl:when test="exists($p/@class)">
			<xsl:variable name="regex" as="xs:string" select="concat('\.', $p/@class, ' \{[^\}]*text-align: ?([a-z]+)')" />
			<xsl:analyze-string select="$global-styles" regex="{ $regex }">
				<xsl:matching-substring>
					<xsl:sequence select="regex-group(1)"/>
				</xsl:matching-substring>
			</xsl:analyze-string>
		</xsl:when>
	</xsl:choose>
</xsl:function>

<xsl:template match="header//p[not(parent::blockContainer)]">
	<xsl:choose>
		<xsl:when test="empty(preceding-sibling::*) and exists(child::img)">
			<div class="judgment-header__logo">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
				</xsl:apply-templates>
			</div>
		</xsl:when>
		<xsl:when test="exists(child::neutralCitation)">
			<div class="judgment-header__neutral-citation">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
				</xsl:apply-templates>
			</div>
		</xsl:when>
		<xsl:when test="exists(child::docketNumber)">
			<div class="judgment-header__case-number">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
				</xsl:apply-templates>
			</div>
		</xsl:when>
		<xsl:when test="exists(child::courtType)">
			<div class="judgment-header__court">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
				</xsl:apply-templates>
			</div>
		</xsl:when>
		<xsl:when test="exists(child::docDate)">
			<div class="judgment-header__date">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
				</xsl:apply-templates>
			</div>
		</xsl:when>
		<xsl:when test="matches(normalize-space(.), '^- -( -)+$')">
			<div class="judgment-header__line-separator" aria-hidden="true">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
				</xsl:apply-templates>
			</div>
		</xsl:when>
		<xsl:otherwise>
			<xsl:variable name="alignment" as="xs:string?" select="uk:extract-alignment(.)" />
			<xsl:choose>
				<xsl:when test="$alignment = ('center', 'right', 'left')">
					<p>
						<xsl:attribute name="class">
							<xsl:sequence select="concat('judgment-header__pr-', $alignment)" />
						</xsl:attribute>
						<xsl:apply-templates>
							<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
						</xsl:apply-templates>
					</p>
				</xsl:when>
				<xsl:otherwise>
					<xsl:next-match />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="p">
	<p>
		<xsl:apply-templates>
			<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
		</xsl:apply-templates>
	</p>
</xsl:template>

<xsl:template match="level/*/p[@class='Quote']">
	<div class="judgment-body__section">
		<span class="judgment-body__number"></span>
		<div class="judgment-body__text">
			<blockquote>
				<p>
					<xsl:apply-templates>
						<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
					</xsl:apply-templates>
				</p>
			</blockquote>
		</div>
	</div>
</xsl:template>

<xsl:template match="block">
	<p>
		<xsl:apply-templates>
			<xsl:with-param name="is-uppercase" select="uk:is-uppercase(.)" tunnel="yes" />
		</xsl:apply-templates>
	</p>
</xsl:template>

<xsl:template match="num | heading">
	<xsl:call-template name="inline" />
</xsl:template>

<xsl:template match="neutralCitation">
	<span class="ncn-nowrap">
		<xsl:call-template name="inline" />
	</span>
</xsl:template>

<xsl:template match="courtType | docketNumber | docDate">
	<xsl:call-template name="inline" />
</xsl:template>

<xsl:template match="party | role | judge | lawyer">
	<xsl:call-template name="inline" />
</xsl:template>

<xsl:template match="span">
	<xsl:call-template name="inline" />
</xsl:template>

<!-- all of the inline properties the parser produces -->
<xsl:variable name="inline-properties" as="xs:string+" select="('font-family', 'font-size', 'font-weight', 'font-style', 'font-variant', 'color', 'background-color', 'text-transform', 'text-decoration-line', 'text-decoration-style')" />

<xsl:function name="uk:get-combined-inline-styles" as="xs:string*">
	<xsl:param name="e" as="element()" />
	<xsl:variable name="from-class-attr" as="xs:string*">
		<xsl:if test="exists($e/@class)">
			<xsl:variable name="regex" as="xs:string" select="concat('\.', $e/@class, ' \{([^\}]+)')" />
			<xsl:analyze-string select="$global-styles" regex="{ $regex }">
				<xsl:matching-substring>
					<xsl:for-each select="tokenize(regex-group(1), ';')">
						<xsl:variable name="prop" as="xs:string" select="normalize-space(substring-before(., ':'))" />
						<xsl:if test="$prop = $inline-properties">
							<xsl:sequence select="normalize-space(.)" />
						</xsl:if>
					</xsl:for-each>
				</xsl:matching-substring>
			</xsl:analyze-string>
		</xsl:if>
	</xsl:variable>
	<xsl:variable name="from-style-attr" as="xs:string*">
		<xsl:for-each select="tokenize($e/@style, ';')">
			<xsl:variable name="prop" as="xs:string" select="normalize-space(substring-before(., ':'))" />
			<xsl:if test="$prop = $inline-properties">
				<xsl:sequence select="normalize-space(.)" />
			</xsl:if>
		</xsl:for-each>
	</xsl:variable>
	<xsl:variable name="style-properties" as="xs:string*">
		<xsl:for-each select="$from-style-attr">
			<xsl:sequence select="normalize-space(substring-before(., ':'))" />
		</xsl:for-each>
	</xsl:variable>
	<xsl:for-each select="$from-class-attr">
		<xsl:variable name="prop" as="xs:string" select="normalize-space(substring-before(., ':'))" />
		<xsl:if test="not($prop = $style-properties)">
			<xsl:sequence select="." />
		</xsl:if>
	</xsl:for-each>
	<xsl:sequence select="$from-style-attr" />
</xsl:function>

<xsl:template name="inline">
	<xsl:param name="name" as="xs:string" select="'span'" />
	<xsl:param name="styles" as="xs:string*" select="uk:get-combined-inline-styles(.)" />
	<xsl:param name="is-uppercase" as="xs:boolean" select="false()" tunnel="yes" />
	<xsl:variable name="styles" as="xs:string*" select="$styles[not(starts-with(., 'font-size:'))]" />
	<xsl:variable name="styles" as="xs:string*" select="$styles[not(starts-with(., 'font-family:')) or contains(., 'Symbol') or contains(., 'Wingdings')]" />
	<xsl:choose>
		<xsl:when test="exists($styles[starts-with(., 'font-weight:') and not(starts-with(., 'font-weight:normal'))])">
			<b>
				<xsl:if test="exists($styles[starts-with(., 'font-weight:') and not(starts-with(., 'font-weight:bold'))])">
					<xsl:attribute name="style">
						<xsl:value-of select="string-join($styles[starts-with(., 'font-weight:')], ';')" />
					</xsl:attribute>
				</xsl:if>
				<xsl:call-template name="inline">
					<xsl:with-param name="name" select="$name" />
					<xsl:with-param name="styles" select="$styles[not(starts-with(., 'font-weight:'))]" />
				</xsl:call-template>
			</b>
		</xsl:when>
		<xsl:when test="exists($styles[starts-with(., 'font-style:') and not(starts-with(., 'font-style:normal'))])">
			<i>
				<xsl:if test="exists($styles[starts-with(., 'font-style:') and not(starts-with(., 'font-style:italic'))])">
					<xsl:attribute name="style">
						<xsl:value-of select="string-join($styles[starts-with(., 'font-style:')], ';')" />
					</xsl:attribute>
				</xsl:if>
				<xsl:call-template name="inline">
					<xsl:with-param name="name" select="$name" />
					<xsl:with-param name="styles" select="$styles[not(starts-with(., 'font-style:'))]" />
				</xsl:call-template>
			</i>
		</xsl:when>
		<xsl:when test="exists($styles[starts-with(., 'text-decoration-line:') and not(starts-with(., 'text-decoration-line:none'))])">
			<u>
				<xsl:if test="exists($styles[starts-with(., 'text-decoration-line:') and not(starts-with(., 'text-decoration-line:underline'))])">
					<xsl:attribute name="style">
						<xsl:value-of select="string-join($styles[starts-with(., 'text-decoration-')], ';')" />
					</xsl:attribute>
				</xsl:if>
				<xsl:call-template name="inline">
					<xsl:with-param name="name" select="$name" />
					<xsl:with-param name="styles" select="$styles[not(starts-with(., 'text-decoration-'))]" />
				</xsl:call-template>
			</u>
		</xsl:when>
		<xsl:when test="exists($styles)">
			<xsl:element name="{ $name }">
				<xsl:attribute name="style">
					<xsl:value-of select="string-join($styles, ';')" />
				</xsl:attribute>
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(., $is-uppercase)" tunnel="yes" />
				</xsl:apply-templates>
			</xsl:element>
		</xsl:when>
		<xsl:when test="$name = 'span'">
			<xsl:apply-templates>
				<xsl:with-param name="is-uppercase" select="uk:is-uppercase(., $is-uppercase)" tunnel="yes" />
			</xsl:apply-templates>
		</xsl:when>
		<xsl:otherwise>
			<xsl:element name="{ $name }">
				<xsl:apply-templates>
					<xsl:with-param name="is-uppercase" select="uk:is-uppercase(., $is-uppercase)" tunnel="yes" />
				</xsl:apply-templates>
			</xsl:element>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="img">
	<img>
		<xsl:apply-templates select="@*" />
		<xsl:apply-templates />
	</img>
</xsl:template>
<xsl:template match="img/@src">
	<xsl:attribute name="src">
		<xsl:sequence select="concat($image-base, $doc-id, '/', .)" />
	</xsl:attribute>
</xsl:template>

<xsl:template match="img/@style">
	<xsl:next-match>
		<xsl:with-param name="properties" select="('width', 'height')" />
	</xsl:next-match>
</xsl:template>

<xsl:template match="br">
	<br />
</xsl:template>

<xsl:template match="date">
	<xsl:call-template name="inline" />
</xsl:template>


<!-- tables -->

<xsl:template match="table">
	<table>
		<xsl:variable name="header-rows" as="element()*" select="*[child::th]" />
		<xsl:if test="exists($header-rows)">
			<thead>
				<xsl:apply-templates select="$header-rows" />
			</thead>
		</xsl:if>
		<tbody>
			<xsl:apply-templates select="* except $header-rows" />
		</tbody>
	</table>
</xsl:template>

<xsl:template match="tr | th | td">
	<xsl:element name="{ local-name() }">
		<xsl:copy-of select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<!-- header tables -->

<xsl:template match="header//table">
	<xsl:choose>
		<xsl:when test="every $row in * satisfies uk:can-remove-first-column($row)">
			<xsl:apply-templates select="." mode="remove-first-column" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:next-match />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:function name="uk:can-remove-first-column" as="xs:boolean">
	<xsl:param name="row" as="element()" />
	<xsl:sequence select="count($row/*) = 3 and uk:cell-is-empty($row/*[1])" />
</xsl:function>

<xsl:function name="uk:cell-is-empty" as="xs:boolean">
	<xsl:param name="cell" as="element()" />
	<xsl:sequence select="empty($cell/@colspan) and empty($cell/@rowspan) and not(normalize-space(string($cell)))" />
</xsl:function>

<xsl:template match="table" mode="remove-first-column">
	<table class="pr-two-column">
		<tbody>
			<xsl:apply-templates mode="remove-first-column" />
		</tbody>
	</table>
</xsl:template>

<xsl:template match="tr" mode="remove-first-column">
	<tr>
		<xsl:copy-of select="@*" />
		<xsl:apply-templates select="*[position() gt 1]" />
	</tr>
</xsl:template>


<!-- links -->

<xsl:template match="a | ref">
	<xsl:choose>
		<xsl:when test="uk:link-is-supported(@href)">
			<a>
				<xsl:apply-templates select="@href" />
				<xsl:apply-templates />
			</a>
		</xsl:when>
		<xsl:otherwise>
			<xsl:apply-templates />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<!-- tables of contents -->

<xsl:template match="toc">
	<div>
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="tocItem">
	<p>
		<xsl:apply-templates />
	</p>
</xsl:template>


<!-- markers and attributes -->

<xsl:template match="marker[@name='tab']">
	<span>
		<xsl:text> </xsl:text>
	</span>
</xsl:template>

<xsl:template match="@style">
	<xsl:param name="properties" as="xs:string*" select="('font-weight', 'font-style', 'text-transform', 'font-variant', 'text-decoration-line', 'text-decoration-style')" />
	<xsl:variable name="values" as="xs:string*">
		<xsl:for-each select="tokenize(., ';')">
			<xsl:if test="tokenize(., ':')[1] = $properties">
				<xsl:sequence select="." />
			</xsl:if>
		</xsl:for-each>
	</xsl:variable>
	<xsl:if test="exists($values)">
		<xsl:attribute name="style">
			<xsl:sequence select="string-join($values, ';')" />
		</xsl:attribute>
	</xsl:if>
</xsl:template>

<xsl:template match="@src | @href | @title">
	<xsl:copy />
</xsl:template>

<xsl:template match="@class | @refersTo | @date | @as" />

<xsl:template match="@*" />


<!-- footnotes -->

<xsl:template match="authorialNote">
	<sup>
		<xsl:value-of select="@marker" />
	</sup>
</xsl:template>

<xsl:template name="footnotes">
	<xsl:param name="footnotes" as="element()*" select="descendant::authorialNote" />
	<xsl:if test="exists($footnotes)">
		<footer>
			<hr />
			<xsl:apply-templates select="$footnotes" mode="footnote" />
		</footer>
	</xsl:if>
</xsl:template>

<xsl:template match="authorialNote" mode="footnote">
	<div>
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="authorialNote/p[1]">
	<p>
		<sup>
			<xsl:value-of select="../@marker" />
		</sup>
		<xsl:text> </xsl:text>
		<xsl:apply-templates />
	</p>
</xsl:template>


<!-- math -->

<xsl:template match="math:*">
	<xsl:copy>
		<xsl:copy-of select="@*"/>
		<xsl:apply-templates />
	</xsl:copy>
</xsl:template>


<!-- text -->

<xsl:function name="uk:is-uppercase" as="xs:boolean">
	<xsl:param name="p" as="element()" />
	<xsl:sequence select="uk:is-uppercase($p, false())" />
</xsl:function>

<xsl:function name="uk:is-uppercase" as="xs:boolean">
	<xsl:param name="e" as="element()" />
	<xsl:param name="default" as="xs:boolean" />
	<xsl:variable name="class-regex-1" as="xs:string" select="concat('\.', $e/@class, ' \{[^\}]*text-transform:')" />
	<xsl:variable name="class-regex-2" as="xs:string" select="concat($class-regex-1, ' ?uppercase')" />
	<xsl:choose>
		<xsl:when test="exists($e/@style) and contains($e/@style, 'text-transform:')">
			<xsl:sequence select="matches($e/@style, 'text-transform: *uppercase')" />
		</xsl:when>
		<xsl:when test="exists($e/@class) and matches($global-styles, $class-regex-1)">
			<xsl:sequence select="matches($global-styles, $class-regex-2)"/>
		</xsl:when>
		<xsl:otherwise>
			<xsl:sequence select="$default" />
		</xsl:otherwise>
	</xsl:choose>
</xsl:function>

<xsl:template match="text()">
	<xsl:param name="is-uppercase" as="xs:boolean" select="false()" tunnel="yes" />
	<xsl:choose>
		<xsl:when test="$is-uppercase">
			<xsl:value-of select="upper-case(.)" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:copy />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

</xsl:transform>
