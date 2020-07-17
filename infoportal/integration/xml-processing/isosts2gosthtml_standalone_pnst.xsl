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

  <xsl:import href="isosts2gosthtml_standalone_rst.xsl"/>

  <xsl:template name="dates">
    <p class="implement_date">Срок действия с <xsl:value-of select=".//reg-meta/meta-date[@type='implementation'][1]/text()"/><br/>до <xsl:value-of select=".//reg-meta/meta-date[@type='termination'][1]/text()"/></p>
  </xsl:template>

</xsl:stylesheet>
