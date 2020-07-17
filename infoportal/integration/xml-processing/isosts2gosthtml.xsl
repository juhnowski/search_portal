<?xml version="1.0"?>
<!-- ============================================================= -->
<!--  Purpose: Convert ISOSTS XML to XHTML 1.1                     -->
<!--  Author: Holger APEL (apel@iso.org)                           -->
<!--  LastRevision: e1691e3ec3259313cd468e29ad3ce16ddedaa20f       -->
<!--  LastChanged: 2015-05-20 18:40:10                             -->
<!--  Copyright © ISO. All rights reserved.                        -->
<!-- ============================================================= -->
<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  xmlns:tbx="urn:iso:std:iso:30042:ed-1"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  xmlns:mle="http://www.iso.org/ns/mle"
  xmlns:isosts="http://www.iso.org/ns/isosts"
  xmlns:loc="http://www.iso.org/ns/localization"
  xmlns:tmp="http://www.iso.org/ns/tmp"
  xmlns:svg="http://www.w3.org/2000/svg"
  xmlns="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="xs xlink mml tbx xhtml isosts loc mle tmp svg">

  <xsl:import href="isosts2html.xsl"/>

  <xsl:output encoding="UTF-8" omit-xml-declaration="yes" method="xhtml"/>

  <xsl:template match="*/text()[normalize-space()]">
    <xsl:value-of select="normalize-space()"/>
  </xsl:template>

<xsl:template match="*/text()[not(normalize-space())]" />

  <xsl:template name="dates">
    <p class="implement_date">
      Дата введения &#8212;
      <xsl:value-of select=".//meta-date[@type='implementation'][1]/text()"/>
    </p>
  </xsl:template>

  <xsl:template match="xref[not(@ref-type='sec') and not(@ref-type='app')]">
    <a class="sts-xref" href="#{$urn}{replace(@rid,'_','_')}">
      <xsl:choose>
        <xsl:when test="@ref-type='fn'">
          <xsl:attribute name="title">
            <xsl:value-of select="key('element-by-id',@rid)/*[not(self::label)]"/>
          </xsl:attribute>
        </xsl:when>
        <xsl:when test="@ref-type='bibr'">
          <xsl:attribute name="title">
            <xsl:value-of select="key('element-by-id',@rid)/*[not(self::label)]"/>
          </xsl:attribute>
        </xsl:when>
        <xsl:when test="@ref-type='other'">
          <xsl:attribute name="title">
            <xsl:value-of select="string-join(key('element-by-id',@rid)/*, ' ')"/>
          </xsl:attribute>
        </xsl:when>
      </xsl:choose>
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="xref[@ref-type='sec']">
    <a class="sts-xref" href="#{$urn}{@rid}">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="xref[@ref-type='app']">
    <a class="sts-xref" href="#{$urn}{@rid}">
      <xsl:apply-templates/>
    </a>
  </xsl:template>

  <xsl:template match="term-sec">
    <div class="sts-section sts-tbx-sec" id="{tbx:termEntry[1]/@id}">
      <xsl:apply-templates/>
    </div>
    <xsl:choose>
        <xsl:when test="@id">
            <div class="sts-section sts-tbx-sec" id="{tbx:termEntry[1]/@id}">
                <xsl:apply-templates/>
            </div></xsl:when>
        <xsl:otherwise>
            <div class="sts-section sts-tbx-sec">
                <xsl:apply-templates/>
            </div>
        </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="term">
    <td class="def-term">
      <xsl:call-template name="assign-id"/>
      <a href="#">
        <xsl:apply-templates/>
      </a>
    </td>
  </xsl:template>

  <xsl:template match="media">
    <xsl:apply-templates/>
    <img src="{@xlink:href}" width="{@width}" height="{@height}" />
  </xsl:template>

  <xsl:template match="graphic">
    <xsl:apply-templates/>
    <img src="{@xlink:href}" width="{@width}" height="{@height}" />
  </xsl:template>


  <xsl:template match="std/title">
    <span class="sts-std-title"><xsl:apply-templates/></span>
  </xsl:template>


  <xsl:template match="term-sec/label">
    <span class="sts-tbx-label"><xsl:apply-templates/></span>
    <xsl:text> </xsl:text>
  </xsl:template>

  <xsl:template match="tbx:termEntry">
    <span class="sts-tbx-sec-inner {../@display}">
      <xsl:if test="./tbx:langSet[@xml:lang='ru']/tbx:tig/tbx:term/normalize-space()">
        <span class="sts-tbx-term">
          <xsl:apply-templates select="./tbx:langSet[@xml:lang='ru']/tbx:tig/tbx:term"/>
        </span>
        <xsl:if test="./tbx:langSet[not(@xml:lang='ru')]">
          <xsl:text> (</xsl:text>
          <xsl:for-each select="./tbx:langSet[not(@xml:lang='ru')]">
            <xsl:if test="not(position()=1)"><xsl:text>, </xsl:text></xsl:if>
            <span class="sts-tbx-term-lang">
              <xsl:apply-templates select="./tbx:tig/tbx:term"/>
            </span>
          </xsl:for-each>
          <xsl:text>)</xsl:text>
        </xsl:if>
        <xsl:text>: </xsl:text>

        <xsl:apply-templates select=".//tbx:definition[1]"/>

        <xsl:if test=".//tbx:source[1]/normalize-space()">
          <span class="sts-tbx-source">
            <xsl:apply-templates select=".//tbx:source[1]"/>
          </span>
        </xsl:if>
      </xsl:if>
    </span>
  </xsl:template>

  <xsl:template match="tbx:source">
    <div class="sts-tbx-source">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tbx:definition">
    <span class="sts-tbx-def">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <xsl:template match="tbx:term">
      <xsl:apply-templates/>
  </xsl:template>


  <xsl:template match="std[not(title)]" priority="1">
    <xsl:if test="./doc-type">
      <xsl:value-of select="./doc-type/text()"/>
      <xsl:text disable-output-escaping="yes"><![CDATA[&nbsp;]]></xsl:text>
    </xsl:if>
    <xsl:choose>
      <xsl:when test="@std-id">
        <a class="sts-std-ref" target="_blank" href="/document?query={@std-id}"><xsl:apply-templates/></a>
      </xsl:when>
      <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="std-ref[following-sibling::title]|*/std-ref">
    <xsl:if test="./doc-type">
      <xsl:value-of select="./doc-type/text()"/>
      <xsl:text disable-output-escaping="yes"><![CDATA[&nbsp;]]></xsl:text>
    </xsl:if>
    <xsl:choose>
      <xsl:when test="../@std-id|../../@std-id">
        <a class="sts-std-ref" target="_blank" href="/document?query={../@std-id|../../@std-id}"><xsl:apply-templates/></a>
      </xsl:when>
      <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>


  <xsl:template match="ref-list[@content-type='bibl' or ancestor::ref-list[@content-type='bibl']]//std-ref/doc-type">
    <xsl:text></xsl:text>
  </xsl:template>


  <xsl:template match="caption">
    <div class="sts-caption">
      <xsl:apply-templates select="p[not(@style-type='align-right')]|non-normative-note|non-normative-example"/>
      <span>
        <xsl:if test="preceding-sibling::label">
          <xsl:apply-templates select="preceding-sibling::label" mode="caption-label"/>
          <xsl:text>&#x0A;</xsl:text>
          <!-- don't use mdash if label ends with ) -->
          <xsl:if test="not(ends-with(normalize-space(preceding-sibling::label), '—'))">
            <xsl:text>—&#x0A;</xsl:text>
          </xsl:if>
        </xsl:if>
        <xsl:apply-templates select="title"/>
      </span>
      <div class="sts-caption-p-right"><xsl:apply-templates select="p[@style-type='align-right']"/></div>
    </div>
  </xsl:template>

  <xsl:template match="fig-group/fig/caption">
    <div class="fig-group-fig-sts-caption">
      <xsl:if test="preceding-sibling::label">
        <xsl:apply-templates select="preceding-sibling::label" mode="caption-label"/>
        <xsl:text>&#x0A;</xsl:text>
      </xsl:if>
      <xsl:apply-templates select="p|non-normative-note|non-normative-example"/>
      <xsl:apply-templates select="title"/>
    </div>
  </xsl:template>

  <xsl:template match="fig">
    <xsl:variable name="id">
    <xsl:choose>
      <xsl:when test="@id"><xsl:value-of select="@id"/></xsl:when>
      <xsl:otherwise><xsl:value-of select="concat(ancestor::*[@id]/@id,'_',generate-id(.))"/></xsl:otherwise>
    </xsl:choose>
    </xsl:variable>

     <div class="sts-fig" id="$id">
         <xsl:apply-templates select="graphic"/>
         <xsl:apply-templates select="caption"/>
     </div>
  </xsl:template>

  <xsl:template match="fig-group">
    <div class="sts-{local-name()}">
      <div class="sts-{local-name()}-content">
        <xsl:apply-templates select="fig"/>
        <xsl:apply-templates select="label"/>
        <xsl:apply-templates select="caption"/>
      </div>
    </div>
  </xsl:template>

  <xsl:template match="ref-list[@content-type='normref' or ancestor::ref-list[@content-type='normref']]">
    <div class="sts-section sts-ref-list">
      <ul class="sts-ref-list">
        <xsl:for-each select="ref">
            <xsl:choose>
                <xsl:when test="@id"><li id="@id"><xsl:apply-templates/></li></xsl:when>
                <xsl:otherwise><li><xsl:apply-templates/></li></xsl:otherwise>
            </xsl:choose><!--
          <li id="8">
            <xsl:apply-templates/>
          </li>-->
        </xsl:for-each>
      </ul>
    </div>
  </xsl:template>

  <xsl:variable name="sec" select="/standard/body/sec[label/text()!='']"/>
  <xsl:variable name="subsec" select="/standard/body/sec[label/text()!='']/descendant::sec[label/text()!='']"/>
  <xsl:variable name="app" select="/standard/back/app-group/app[label/text()!='']"/>
  <xsl:variable name="ref" select="/standard/back/ref-list"/>

  <xsl:template match="front">

    <xsl:apply-templates select="./sec[@sec-type='foreword'][1]" />
    <xsl:apply-templates select="./notes" />
    <xsl:call-template name="copyright">
      <xsl:with-param name="metadata" select="./iso-meta"/>
    </xsl:call-template>
    <div class="sts-section sts-content-section">
    <h1 class="front-sec-title front-toc-title">Содержание</h1>
      <div id="toc">
        <ol>
          <xsl:for-each select="$sec|$subsec|$app|$ref">
            <!--<tr>-->
                <li>
                    <xsl:if test="count(ancestor::sec)&gt;0">
                        <xsl:for-each select="ancestor::sec">&#160;</xsl:for-each>
                    </xsl:if>
                    <xsl:choose>
                        <xsl:when test="count(parent::app-group)&gt;0">
                            <xsl:value-of select="label/text()"/>
                            <xsl:text>&#160;</xsl:text>
                            <xsl:if test="matches(./label/text(), 'приложение', 'i')">
                                <xsl:value-of select="./annex-type/text()"/>
                                <xsl:text>&#160;</xsl:text>
                            </xsl:if>
                            <a class="sts-xref" href="#{@id}"><xsl:value-of select="title/text()"/>1</a>
                        </xsl:when>
                        <xsl:when test="count(parent::back)&gt;0">
                            <a class="sts-xref" href="#{@id}"><xsl:value-of select="title/text()"/>2</a>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="label/text()"/>&#160;<xsl:variable name="point_text" select="./title/descendant-or-self::*/text()"/>
                            <a class="sts-xref" href="#sec_{label/text()}"><xsl:value-of select="$point_text"/>3</a>
                        </xsl:otherwise>
                    </xsl:choose>
                </li>
            <!--</tr>-->
          </xsl:for-each>
        </ol>
      </div>
    </div>
    <xsl:for-each select="./sec[@sec-type='foreword']">
      <xsl:if test="position() > 1">
        <xsl:apply-templates />
      </xsl:if>
    </xsl:for-each>
    <xsl:apply-templates select="./sec[@sec-type='intro']" />

    <!-- 14 -->
    <div class="first_div">
        <xsl:variable name="doc-lang" select="/standard/front/iso-meta/content-language"/>
        <p class="std_title">
            <xsl:value-of
                    select="//iso-meta/custom-meta-group/custom-meta[meta-name[contains(text(),'Type')]
                     and meta-value[string-length(text()) > 1]]/meta-value/text()"/>
        </p>
        <hr class="first_line" />

        <xsl:if test="normalize-space(/standard/front/iso-meta/title-wrap[@xml:lang=$doc-lang]/intro)">
        <p class="std_name_intro">
            <xsl:value-of select="/standard/front/iso-meta/title-wrap[@xml:lang=$doc-lang]/intro"/>
        </p>
        </xsl:if>

        <xsl:if test="normalize-space(/standard/front/iso-meta/title-wrap[@xml:lang=$doc-lang]/main)">
        <p class="std_name_main">
            <xsl:value-of select="/standard/front/iso-meta/title-wrap[@xml:lang=$doc-lang]/main"/>
        </p>
        </xsl:if>

        <xsl:if test="normalize-space(/standard/front/iso-meta/title-wrap[@xml:lang=$doc-lang]/compl)">
        <p class="std_name_compl">
            <xsl:value-of select="/standard/front/iso-meta/title-wrap[@xml:lang=$doc-lang]/compl"/>
        </p>
        </xsl:if>

        <p class="std_eng_name">
            <xsl:value-of select="/standard/front/iso-meta/title-wrap[@xml:lang='eng']/full"/>
        </p>

        <hr class="second_line" />
        <xsl:call-template name="dates"/>
    </div>

  </xsl:template>

  <xsl:variable name="tables" select="//table"/>

  <xsl:template name='ics-name'>МКС</xsl:template>

  <xsl:template name='ics'>
    <xsl:if test='/standard/front/iso-meta/ics/text()'>
      <td>
          <xsl:call-template name='ics-name'/>&#160;<xsl:for-each select='/standard/front/iso-meta/ics'>
            <xsl:value-of select="text()"/><br/>
            <xsl:text disable-output-escaping="yes"><![CDATA[&emsp;]]></xsl:text>
          </xsl:for-each>
      </td>
    </xsl:if>
  </xsl:template>

  <xsl:template match='/standard/front/iso-meta/custom-meta-group'>
    <hr/>

    <table class="keywords_and_codes">
      <tr>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="udk"])&gt;0'>
          <td>УДК&#160;<xsl:for-each select='./custom-meta/meta-name[lower-case(text())="udk"]'>
              <xsl:value-of select="./following-sibling::meta-value/text()"/>
              <xsl:text disable-output-escaping="yes"><![CDATA[&emsp;]]></xsl:text>
            </xsl:for-each>
          </td>
        </xsl:if>
        <xsl:call-template name='ics'/>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="okpd2"])&gt;0'>
          <td>ОКПД2&#160;<xsl:for-each select='./custom-meta/meta-name[lower-case(text())="okpd2"]'>
              <xsl:value-of select="./following-sibling::meta-value/text()"/>
              <br /><xsl:text disable-output-escaping="yes"><![CDATA[&emsp;]]></xsl:text>
            </xsl:for-each>
          </td>
        </xsl:if>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="kgs"])&gt;0'>
          <td><xsl:for-each select='./custom-meta/meta-name[lower-case(text())="kgs"]'>
              <xsl:value-of select="./following-sibling::meta-value/text()"/>
              <xsl:text disable-output-escaping="yes"><![CDATA[&emsp;]]></xsl:text>
            </xsl:for-each>
          </td>
        </xsl:if>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="okstu"])&gt;0'>
          <td>ОКСТУ&#160;<xsl:for-each select='./custom-meta/meta-name[lower-case(text())="okstu"]'>
              <xsl:value-of select="./following-sibling::meta-value/text()"/>
              <br /><xsl:text disable-output-escaping="yes"><![CDATA[&emsp;]]></xsl:text>
            </xsl:for-each>
          </td>
        </xsl:if>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="okp"])&gt;0'>
          <td>ОКП&#160;<xsl:for-each select='./custom-meta/meta-name[lower-case(text())="okp"]'>
              <xsl:value-of select="./following-sibling::meta-value/text()"/>
              <br /><xsl:text disable-output-escaping="yes"><![CDATA[&emsp;]]></xsl:text>
            </xsl:for-each>
          </td>
        </xsl:if>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="idt"])&gt;0'>
          <td>IDT&#160;<xsl:value-of select="./following-sibling::meta-value/text()"/>
          </td>
        </xsl:if>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="mod"])&gt;0'>
          <td>MOD&#160;<xsl:value-of select="./following-sibling::meta-value/text()"/>
          </td>
        </xsl:if>
        <xsl:if test='count(./custom-meta/meta-name[lower-case(text())="neq"])&gt;0'>
          <td>NEQ&#160;<xsl:value-of select="./following-sibling::meta-value/text()"/>
          </td>
        </xsl:if>
      </tr>
    </table>

    <br/>

    <span>Ключевые слова:&#160;</span>
    <span>
      <xsl:value-of select='./custom-meta/meta-name[lower-case(text())="keywords"]/following-sibling::meta-value'/>&#160;</span>

    <hr/>
  </xsl:template>

  <xsl:template name="copyright">
    <xsl:param name="metadata"/>
    <div class="sts-copyright">
      <xsl:for-each select="$metadata/permissions">
        <div>
            <xsl:text>©&#xA0;</xsl:text><xsl:value-of select="copyright-holder"/>
            <xsl:text>,&#xA0;</xsl:text><xsl:value-of select="copyright-year"/>
        </div>
      </xsl:for-each>
      <xsl:for-each select="$metadata/permissions">
        <xsl:if test="normalize-space(copyright-statement)">
          <div class="sts-copyright-statement"><xsl:value-of select="copyright-statement"/></div>
        </xsl:if>
      </xsl:for-each>
    </div>
  </xsl:template>

  <xsl:template match="non-normative-example/label[following-sibling::p]">
  </xsl:template>

  <xsl:template match="non-normative-example/label[not(following-sibling::p)]">
    <p><span class="sts-non-normative-example-label"><xsl:apply-templates/></span></p>
  </xsl:template>

  <xsl:template match="non-normative-example/p[not(preceding-sibling::*[not(self::label)])]">
    <p>
      <xsl:call-template name="p-style-type"/>
      <xsl:for-each select="preceding-sibling::label">
        <span class="sts-{node-name(parent::node())}-label">
          <xsl:apply-templates/>
        </span>
        <xsl:text> </xsl:text>
      </xsl:for-each>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="front/iso-meta | front/reg-meta | front/nat-meta">
  </xsl:template>

  <xsl:template match="front/sec/title" name="sec-title">
    <xsl:param name="level" select="count(ancestor-or-self::sec)"/>
    <xsl:param name="contents">
      <xsl:apply-templates select="." mode="sec-title"/>
    </xsl:param>
    <xsl:if test="normalize-space($contents)">
      <xsl:element name="{concat('h',$level)}">
      <xsl:attribute name="class">front-sec-title</xsl:attribute>
        <xsl:copy-of select="$contents"/>
      </xsl:element>
    </xsl:if>
  </xsl:template>

  <xsl:template match="title" mode="sec-title">
    <xsl:if test="preceding-sibling::label//text()">
      <xsl:apply-templates select="preceding-sibling::label" mode="sec-title"/>
      <xsl:text>&#xA0;</xsl:text>
    </xsl:if>
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="label" mode="raw-label">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="disp-formula">
    <div class="sts-{local-name()}-panel">
      <xsl:if test="@id">
        <xsl:attribute name="id">
          <xsl:value-of select="@id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:call-template name="named-anchor"/>
      <xsl:apply-templates/>
      <xsl:if test="label">
        <div class="sts-{local-name()}-label"><xsl:apply-templates select="label" mode="raw-label"/></div>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template match="notes">
     <div class="sts-{local-name()}">
         <xsl:apply-templates/>
     </div>
  </xsl:template>

  <xsl:template match="p">
    <p>
      <xsl:if test="@id">
        <xsl:attribute name="id">
          <xsl:value-of select="@id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:call-template name="p-style-type"/>
      <!-- if only label without title, the label will just be added to the p as starting text -->
      <xsl:if test="(parent::sec or parent::list-item) and preceding-sibling::*[1][self::label]">
      </xsl:if>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="non-normative-note/label[following-sibling::p]">
    <p><span class="sts-non-normative-note-label"><xsl:apply-templates/></span></p>
  </xsl:template>

</xsl:stylesheet>
