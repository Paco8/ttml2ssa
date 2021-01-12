#!/usr/bin/php -q
<?php
?>
# XBMC Media Center language file
# Addon Name: Ttml2Ssa
# Addon id: script.module.ttml2ssa
# Addon version: 0.1.1
# Addon Provider: Paco8
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: XBMC-Addons\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2020-12-28 16:47+0100\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE\n"
"Language: en\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

<?php
$n = 32000;

$l = array('SSA Style', 
           'Font name', 'Font size', 
           'Primary colour (AABBGGRR)', 'Back colour (AABBGGRR)', 'Outline colour (AABBGGRR)',
           'Border style', 'Outline', 'Shadow',
           'Vertical margin', 'Left margin', 'Right margin',
           'Misc',
           'Allow cosmetic changes', 'Allow fixes for some languages',
           'Timestamp minimum separation (SSA only) in ms',
           'Outline with shadow', 'Opaque box',
           'Bold', 'Italic',
           'Allow italics', 'Allow text on the top');

foreach ($l as $i) {
	echo "msgctxt \"#$n\"\n";
	echo "msgid \"$i\"\n";
	echo "msgstr \"\"\n\n";

	$n++;
}
?>
