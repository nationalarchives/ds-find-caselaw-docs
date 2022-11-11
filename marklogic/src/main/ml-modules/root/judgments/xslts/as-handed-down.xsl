<?xml version="1.0" encoding="utf-8"?>

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	xpath-default-namespace="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
	xmlns:uk1="https:/judgments.gov.uk/"
	xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn"
	xmlns:html="http://www.w3.org/1999/xhtml"
	xmlns:math="http://www.w3.org/1998/Math/MathML"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="uk1 uk html math xs">

<xsl:output method="html" encoding="utf-8" indent="no" include-content-type="no" />

<xsl:strip-space elements="*" />
<xsl:preserve-space elements="p block num heading span a courtType date docDate docTitle docketNumber judge lawyer location neutralCitation party role time" />

<xsl:param name="standalone" as="xs:boolean" select="false()" />
<xsl:param name="image-base" as="xs:string" select="'/'" />
<xsl:param name="suppress-links" as="xs:boolean" select="true()" />

<!-- functions -->

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

<!-- global variables -->

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

<xsl:variable name="title" as="xs:string?">
	<xsl:sequence select="/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRname/@value" />
</xsl:variable>

<!-- templates -->

<xsl:template match="akomaNtoso">
	<xsl:choose>
		<xsl:when test="$standalone">
			<html>
				<head>
					<title>
						<xsl:value-of select="$title" />
					</title>
					<style>
						<xsl:text>
body { margin: 1cm 1in }
</xsl:text>
						<xsl:call-template name="style" />
					</style>
				</head>
				<body>
					<xsl:apply-templates />
				</body>
			</html>
		</xsl:when>
		<xsl:otherwise>
			<div id="judgment-wrapper">
				<xsl:apply-templates />
			</div>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="meta" />

<xsl:variable name="selector1" as="xs:string" select="if ($standalone) then 'body' else '#judgment-wrapper'" />

<xsl:template name="style">
<xsl:value-of select="$selector1" /> .tab { display: inline-block; width: 0.25in }
<xsl:value-of select="$selector1" /> section { position: relative }
<xsl:value-of select="$selector1" /> h2 { font-size: inherit; font-weight: normal }
<xsl:value-of select="$selector1" /> h2.floating { position: absolute; margin-top: 0 }
<xsl:value-of select="$selector1" /> .num { display: inline-block; padding-right: 1em }
<xsl:value-of select="$selector1" /> td { position: relative; min-width: 2em; padding-left: 1em; padding-right: 1em; vertical-align: top }
<xsl:value-of select="$selector1" /> td > .num { left: -2em }
<xsl:value-of select="$selector1" /> table { margin: 0 auto; width: 100%; border-collapse: collapse }
<xsl:value-of select="$selector1" /> .header table { table-layout: fixed }
<xsl:value-of select="$selector1" /> td > p:first-child { margin-top: 0 }
<xsl:value-of select="$selector1" /> td > p:last-child { margin-bottom: 0 }
<xsl:value-of select="$selector1" /> .fn { vertical-align: super; font-size: small }
<xsl:value-of select="$selector1" /> .footnote > p > .marker { vertical-align: super; font-size: small }
<xsl:value-of select="$selector1" /> .restriction { color: red }
<xsl:apply-templates select="/akomaNtoso/judgment/meta/presentation/html:style" />
<xsl:apply-templates select="/akomaNtoso/judgment/attachments/attachment/doc/meta/presentation/html:style" />
<xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="html:style">
	<xsl:value-of select="." />
</xsl:template>

<xsl:template match="judgment">
	<article id="judgment">
		<xsl:apply-templates />
		<xsl:apply-templates select="attachments/attachment/doc[@name=('annex','schedule')]" />
		<xsl:call-template name="footnotes">
			<xsl:with-param name="footnotes" as="element()*">
				<xsl:sequence select="header//authorialNote" />
				<xsl:sequence select="judgmentBody//authorialNote" />
				<xsl:sequence select="attachments/attachment/doc[@name=('annex','schedule')]//authorialNote" />
			</xsl:with-param>
		</xsl:call-template>
	</article>
	<xsl:apply-templates select="attachments/attachment/doc[not(@name=('annex','schedule'))]" />
</xsl:template>

<xsl:template match="attachments" />

<xsl:template match="coverPage | header">
	<div class="{ local-name() }">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="judgmentBody">
	<div class="body">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="doc[@name=('annex','schedule')]">
	<section>
		<xsl:attribute name="id"><!-- not needed for CSS -->
			<xsl:value-of select="@name" />
			<xsl:if test="exists(../preceding-sibling::*[@name=current()/@name]) or exists(../following-sibling::*[@name=current()/@name])">
				<xsl:value-of select="count(../preceding-sibling::*[@name=current()/@name]) + 1" />
			</xsl:if>
		</xsl:attribute>
		<xsl:apply-templates />
	</section>
</xsl:template>

<xsl:template match="doc[not(@name=('annex','schedule'))]">
	<xsl:variable name="id" as="xs:string"><!-- must match selector in XML presentation element -->
		<xsl:choose>
			<xsl:when test="@name = 'attachment'"> <!-- for backwards compatibility -->
				<xsl:sequence select="concat(@name, string(count(../preceding-sibling::*) + 1))" />
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="work-this" as="xs:string" select="meta/identification/FRBRWork/FRBRthis/@value" />
				<xsl:variable name="parts" as="xs:string*" select="tokenize($work-this, '/')" />
				<xsl:variable name="last-two-parts" as="xs:string*" select="subsequence($parts, count($parts) - 1)" />
				<xsl:sequence select="string-join($last-two-parts, '')" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<article id="{ $id }">
		<xsl:apply-templates />
		<xsl:call-template name="footnotes" />
	</article>
</xsl:template>

<xsl:template match="doc[not(@name=('annex','schedule'))]/mainBody">
	<div class="body">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template name="class">
	<xsl:attribute name="class">
		<xsl:value-of select="local-name()" />
		<xsl:if test="@class">
			<xsl:text> </xsl:text>
			<xsl:value-of select="@class" />
		</xsl:if>
	</xsl:attribute>
</xsl:template>

<xsl:template match="decision">
	<xsl:choose>
		<xsl:when test="exists(preceding-sibling::*) or exists(following-sibling::*)">
			<section class="decision">
				<xsl:if test="exists(@eId)">
					<xsl:attribute name="id">
						<xsl:value-of select="@eId" />
					</xsl:attribute>
				</xsl:if>
				<xsl:apply-templates />
			</section>
		</xsl:when>
		<xsl:otherwise>
			<xsl:next-match />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="level | paragraph | subparagraph">
	<section>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:if test="num | heading">
			<h2>
				<xsl:choose>
					<xsl:when test="exists(heading/@class)">
						<xsl:attribute name="class">
							<xsl:value-of select="heading/@class" />
						</xsl:attribute>
					</xsl:when>
					<xsl:when test="empty(heading)">
						<xsl:attribute name="class">floating</xsl:attribute>
					</xsl:when>
				</xsl:choose>
				<xsl:apply-templates select="num | heading" />
			</h2>
		</xsl:if>
		<xsl:apply-templates select="* except (num, heading)" />
	</section>
</xsl:template>

<!-- <xsl:template match="hcontainer[@name='tableOfContents']" /> -->

<xsl:template match="blockContainer">
	<section>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates select="* except num" />
	</section>
</xsl:template>

<xsl:template match="blockContainer/p[1]">
	<p>
		<xsl:apply-templates select="@*" />
		<xsl:apply-templates select="preceding-sibling::num" />
		<xsl:apply-templates />
	</p>
</xsl:template>

<xsl:template match="p | span">
	<xsl:element name="{ local-name() }">
		<xsl:apply-templates select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="block">
	<p>
		<xsl:attribute name="class">
			<xsl:value-of select="@name" />
			<xsl:if test="@class">
				<xsl:text> </xsl:text>
				<xsl:value-of select="@class" />
			</xsl:if>
		</xsl:attribute>
		<xsl:apply-templates select="@* except @name, @class" />
		<xsl:apply-templates />
	</p>
</xsl:template>

<xsl:template match="num | heading">
	<span>
		<xsl:attribute name="class">
			<xsl:value-of select="local-name()" />
		</xsl:attribute>
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="neutralCitation | courtType | docketNumber | docDate">
	<span>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>

<xsl:template match="party | role | judge | lawyer">
	<span>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
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

<xsl:template match="br">
	<xsl:element name="{ local-name() }">
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="date">
	<span>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</span>
</xsl:template>


<!-- tables -->

<xsl:template match="table">
	<table>
		<xsl:copy-of select="@class | @style" />
		<xsl:if test="exists(@uk1:widths)">
			<colgroup>
				<xsl:for-each select="tokenize(@uk1:widths, ' ')">
					<col style="width:{.}" />
				</xsl:for-each>
			</colgroup>
		</xsl:if>
		<xsl:if test="exists(@uk:widths)">
			<colgroup>
				<xsl:for-each select="tokenize(@uk:widths, ' ')">
					<col style="width:{.}" />
				</xsl:for-each>
			</colgroup>
		</xsl:if>
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

<xsl:template match="tr | th| td">
	<xsl:element name="{ local-name() }">
		<xsl:copy-of select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>


<!-- links -->

<xsl:template match="a | ref">
	<xsl:choose>
		<xsl:when test="not($suppress-links) or uk:link-is-supported(@href)">
			<a>
				<xsl:apply-templates select="@*" />
				<xsl:apply-templates />
			</a>
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="." />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<!-- tables of contents -->

<xsl:template match="toc">
	<div>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="tocItem">
	<p>
		<xsl:call-template name="class" />
		<xsl:apply-templates select="@* except @class" />
		<xsl:apply-templates />
	</p>
</xsl:template>


<!-- markers and attributes -->

<xsl:template match="marker[@name='tab']">
	<span class="tab">
		<xsl:text> </xsl:text>
	</span>
</xsl:template>

<xsl:template match="@eId">
	<xsl:attribute name="id">
		<xsl:sequence select="." />
	</xsl:attribute>
</xsl:template>

<xsl:template match="@class | @style | @src | @href | @title">
	<xsl:copy />
</xsl:template>

<xsl:template match="@refersTo | @date | @as" />

<xsl:template match="@*" />


<!-- footnotes -->

<xsl:template match="authorialNote">
	<span class="fn">
		<xsl:value-of select="@marker" />
	</span>
</xsl:template>

<xsl:template name="footnotes">
	<xsl:param name="footnotes" as="element()*" select="descendant::authorialNote" />
	<xsl:if test="exists($footnotes)">
		<footer class="footnotes">
			<hr style="margin-top:2em" />
			<xsl:apply-templates select="$footnotes" mode="footnote" />
		</footer>
	</xsl:if>
</xsl:template>

<xsl:template match="authorialNote" mode="footnote">
	<div class="footnote">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="authorialNote/p[1]">
	<xsl:element name="{ local-name() }">
		<xsl:apply-templates select="@*" />
		<span class="marker">
			<xsl:value-of select="../@marker" />
		</span>
		<xsl:text> </xsl:text>
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>


<!-- math -->

<xsl:template match="math:*">
	<xsl:copy>
		<xsl:copy-of select="@*"/>
		<xsl:apply-templates />
	</xsl:copy>
</xsl:template>

</xsl:transform>
