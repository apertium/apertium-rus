<?xml version="1.0" encoding="UTF-8"?> <!-- -*- nxml -*- -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="UTF-8"/>


  <xsl:preserve-space elements="*"/>

<xsl:template match="s">
  <s n="{./@n}"/>
</xsl:template>

<xsl:template match="a">
  <a/>
</xsl:template>

<xsl:template match="b">
  <b/>
</xsl:template>

<xsl:template match="g">
  <g><xsl:apply-templates/></g>
</xsl:template>

<xsl:template match="a">
  <a/>
</xsl:template>

<xsl:template match="j">
  <j/>
</xsl:template>

<xsl:template match="l">
  <!--<xsl:apply-templates select="./*|text(),'а́','а'"/>-->

<l><xsl:value-of select="translate(./*|text(), 'а́', 'а')" /></l>
<!--<l><xsl:for-each select="*|text()"><xsl:choose><xsl:when test="text()"><xsl:value-of select="translate(., 'а́', 'а')" /></xsl:when> <xsl:otherwise><xsl:copy-of select="." /></xsl:otherwise></xsl:choose></xsl:for-each></l>-->
</xsl:template>

<xsl:template match="r">
  <r><xsl:apply-templates select="./*|text()"/></r>
</xsl:template>

<xsl:template match="par">
  <par n="{./@n}"/>
</xsl:template>

<xsl:template match="re">
  <re><xsl:apply-templates/></re>
</xsl:template>

<xsl:template match="p">
  <p><xsl:apply-templates/></p>
</xsl:template>

<xsl:template match="i">
  <p><l><xsl:value-of select="translate(./*|text(), 'а́', 'а')"/></l><r><xsl:apply-templates select="*|text()"/></r></p>
</xsl:template>

<xsl:template match="e | @*">
    <xsl:copy>
        <xsl:apply-templates select="node() | @*"/>
    </xsl:copy>
</xsl:template>


<xsl:template match="dictionary">
<dictionary>
  <xsl:value-of select="string('&#xA;')"/>
  <xsl:copy-of select="./alphabet"/>
  <xsl:value-of select="string('&#xA;')"/>
  <xsl:copy-of select="./sdefs"/>
  <xsl:value-of select="string('&#xA;')"/>
  <xsl:if test="not(count(./pardefs/pardef)=0)">
    <pardefs>
  <xsl:value-of select="string('&#xA;')"/>

      <xsl:for-each select="./pardefs/pardef">
  <xsl:value-of select="string('&#xA;')"/>

	<pardef n="{./@n}">
	  <xsl:apply-templates/>
	</pardef>
      </xsl:for-each>
  <xsl:value-of select="string('&#xA;')"/>

    </pardefs>
  </xsl:if>
  <xsl:value-of select="string('&#xA;')"/>

  <xsl:for-each select="./section">
    <section id="{./@id}" type="{./@type}">
      <xsl:apply-templates/>
    </section>

  </xsl:for-each>

</dictionary>

</xsl:template>


</xsl:stylesheet>

