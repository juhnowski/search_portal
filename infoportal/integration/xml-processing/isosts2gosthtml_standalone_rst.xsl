<?xml version="1.0" encoding="UTF-8"?>
<!-- ============================================================= -->
<!--  Purpose: Convert ISOSTS XML to XHTML 1.1 standalone document -->
<!--  $LastChangedRevision: 48666 $                                -->
<!--  $LastChangedDate: 2013-10-16 18:19:35 +0200 (Wed, 16 Oct 2013) $                                           -->
<!--                                                               -->
<!-- ============================================================= -->
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:xlink="http://www.w3.org/1999/xlink" 
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  xmlns:tbx="urn:iso:std:iso:30042:ed-1" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:isosts="http://www.iso.org/ns/isosts" 
  xmlns:loc="http://www.iso.org/ns/localization"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:functx="http://www.functx.com"
  xmlns="http://www.w3.org/1999/xhtml" 
  exclude-result-prefixes="xlink mml tbx isosts loc xhtml xs">

  <xsl:import href="isosts2gosthtml_standalone.xsl"/>

  <xsl:template name="header-with-logo">
    <div class="header-with-logo">
      <table>
        <tbody>
          <tr>
            <td class="header-logo">
              <img src="/static/img/scheme/rst-logo.svg"/>
            </td>
            <td class="header-standard">
              <xsl:value-of
                  select="//iso-meta/custom-meta-group/custom-meta[meta-name[contains(text(),'Type')]
                    and meta-value[string-length(text()) > 1]]/meta-value/text()"
              />
            </td>
            <td class="header-code">
              <h1><xsl:value-of select="/standard/front/iso-meta/std-ref[@type='dated']"/></h1>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </xsl:template>

  <xsl:template name='ics-name'>ОКС</xsl:template>

</xsl:stylesheet>
