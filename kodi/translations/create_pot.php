#!/usr/bin/php -q
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
function print_section($l, $n) {
    foreach ($l as $i) {
        echo "msgctxt \"#$n\"\n";
        echo "msgid \"$i\"\n";
        echo "msgstr \"\"\n\n";
        $n++;
    }
}

$style =  array('SSA Style', 
            'Font name', 'Font size', 
            'Primary colour (AABBGGRR)', 'Back colour (AABBGGRR)', 'Outline colour (AABBGGRR)',
            'Border style',
            'Outline with shadow', 'Opaque box',
            'Outline', 'Shadow',
            'Bold', 'Italic',
            'Vertical margin', 'Left margin', 'Right margin',
            'Main');

$misc = array('Misc',
            'Allow italics', 'Allow text on the top',
            'Allow cosmetic changes', 'Allow fixes for some languages',
            'Timestamp minimum separation (SSA only) in ms');

$addons = array('Subtitle type',
            'Improved Subtitles Settings',
            'Improved subtitles',
            'Normal (SRT)', 'Improved (SSA)', 'Both');

print_section($style, 32000);
print_section($misc, 32100);
print_section($addons, 32200);
?>
