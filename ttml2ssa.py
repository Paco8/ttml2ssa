#!/usr/bin/env python
# encoding: utf-8
#
#  --------------------------------------------
#  based on https://github.com/yuppity/ttml2srt
#  --------------------------------------------
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals, absolute_import, division

try:
    from defusedxml import minidom  # type: ignore
except:
    from xml.dom import minidom

import re
import os.path
from collections import OrderedDict

class TimestampConverter(object):

    def __init__(self, frame_rate=23.976, tick_rate=1):
        self.tick_rate = tick_rate
        self.frame_rate = frame_rate

    def timeexpr_to_ms(self, *args):
        return self._timeexpr_to_ms(*args)

    def _timeexpr_to_ms(self, time_expr):
        """Use the given time expression to get a matching conversion method
        to overwrite self.timeexpr_to_ms() with.
        """

        self.timeexpr_to_ms = self.determine_ms_convfn(time_expr)
        return self.timeexpr_to_ms(time_expr)

    def _hhmmss_to_ms(self, hh, mm, ss):
        return hh * 3600 * 1000 + mm * 60 * 1000 + ss * 1000

    def subrip_to_ms(self, timestamp):
        """Desconstruct SubRip timecode down to milliseconds
        """

        hh, mm, ss, ms = re.split(r'[:,]', timestamp)
        return int(int(hh) * 3.6e6 + int(mm) * 60000 + int(ss) * 1000 + int(ms))

    def _metric_to_ms(self, metric_multiplier, metric_value):
        return int(metric_multiplier * metric_value)

    def _ms_to_hhmmssms(self, ms):
        hh = int(ms / 3.6e6)
        mm = int((ms % 3.6e6) / 60000)
        ss = int((ms % 60000) / 1000)
        ms = int(ms % 1000)

        return hh, mm, ss, ms

    def ms_to_subrip(self, ms):
        """Build SubRip timecode from milliseconds
        """

        hh, mm, ss, ms = self._ms_to_hhmmssms(ms)
        return '{:02d}:{:02d}:{:02d},{:03d}'.format(hh, mm, ss, ms)

    def ms_to_ssa(self, ms):
        """Build SSA/ASS timecode from milliseconds
        """

        hh, mm, ss, ms = self._ms_to_hhmmssms(ms)
        return '{:01d}:{:02d}:{:02d}.{:02d}'.format(hh, mm, ss, int(ms / 10))

    def frames_to_ms(self, frames):
        """Convert frame count to ms
        """

        return int(int(frames) * (1000 / self.frame_rate))

    def offset_frames_to_ms(self, time):
        """Convert offset-time expression with f metric to milliseconds.
        """

        frames = float(time[:-1])
        return int(int(frames) * (1000 / self.frame_rate))

    def offset_ticks_to_ms(self, time):
        """Convert offset-time expression with t metric to milliseconds.
        """

        ticks = int(time[:-1])
        seconds = 1.0 / self.tick_rate
        return (seconds * ticks) * 1000

    def offset_hours_to_ms(self, time):
        """Convert offset-time expression with h metric to milliseconds.
        """

        hours = float(time[:-1])
        return self._metric_to_ms(3.6e6, hours)

    def offset_minutes_to_ms(self, time):
        """Convert offset-time expression with m metric to milliseconds.
        """

        return self._metric_to_ms(60 * 1000, float(time[:-1]))

    def offset_seconds_to_ms(self, time):
        """Convert offset-time expression with s metric to milliseconds.
        """

        seconds = float(time[:-1])
        return self._metric_to_ms(1000, seconds)

    def offset_ms_to_ms(self, time):
        """Convert offset-time expression with ms metric to milliseconds.
        """

        ms = int(time[:-2])
        return ms

    def fraction_timestamp_to_ms(self, timestamp):
        """Convert hh:mm:ss.fraction to milliseconds
        """

        hh, mm, ss, fraction = re.split(r'[:.]', timestamp)
        hh, mm, ss = [int(i) for i in (hh, mm, ss)]
        # Resolution beyond ms is useless for our purposes
        ms = int(fraction[:3])

        return self._hhmmss_to_ms(hh, mm, ss) + ms

    def frame_timestamp_to_ms(self, timestamp):
        """Convert hh:mm:ss:frames to milliseconds

        Will handle hh:mm:ss:frames.sub-frames by discarding the sub-frame part
        """

        hh, mm, ss, frames = [int(i) for i in timestamp.split('.')[0].split(':')]
        hhmmss_ms = self._hhmmss_to_ms(hh, mm, ss)
        ms = self.frames_to_ms(frames)
        return hhmmss_ms + ms

    def determine_ms_convfn(self, time_expr):
        """Determine approriate ms conversion fn to pass the time expression to.

        Args:
            time_exrp (str): TTML time expression

        Return:
            Conversion method (callable)

        Strips the time expression of digits and uses the resulting string as
        a key to a dict of conversion methods.
        """

        # Map time expression delimiters to conversion methods. Saves
        # us from having to exec multibranch code on each line but assumes all
        # time expressions to be of the same form.
        time_expr_fns = {

            # clock-time, no frames or fraction
            # Example(s): "00:02:23"
            '::': self.frame_timestamp_to_ms,

            # clock-time, frames
            # Example(s): "00:02:23:12", "00:02:23:12.222"
            ':::': self.frame_timestamp_to_ms,
            ':::.': self.frame_timestamp_to_ms,

            # clock-time, fraction
            # Example(s): "00:02:23.283"
            '::.': self.fraction_timestamp_to_ms,

            # offset-time, hour metric
            # Example(s): "1h", "1.232837372637h"
            'h': self.offset_hours_to_ms,
            '.h': self.offset_hours_to_ms,

            # offset-time, minute metric
            # Example(s): "1m", "13.72986323m"
            'm': self.offset_minutes_to_ms,
            '.m': self.offset_minutes_to_ms,

            # offset-time, second metric
            # Example(s): "1s", "113.2312312s"
            's': self.offset_seconds_to_ms,
            '.s': self.offset_seconds_to_ms,

            # offset-time, millisecond metric
            # Example(s): "1ms", "1000.1231231231223ms"
            'ms': self.offset_ms_to_ms,
            '.ms': self.offset_ms_to_ms,

            # offset-time, frame metric
            # Example(s): "100f"
            'f': self.offset_frames_to_ms,
            '.f': self.offset_frames_to_ms,

            # offset-time, tick metric
            # Example(s): "19298323t"
            't': self.offset_ticks_to_ms,
            '.t': self.offset_ticks_to_ms,

        }

        try:
            delims = ''.join([i for i in time_expr if not i.isdigit()])
            return time_expr_fns[delims]
        except KeyError:
            raise NotImplementedError(
                'Unknown timestamp format ("{}")'.format(time_expr))


class Ttml2Ssa(object):

    VERSION = '0.1.8'

    TIME_BASES = [
        'media',
        'smpte',
    ]

    SCALE = {
        'NTSC2PAL' : 23.976/25,
        'PAL2NTSC' : 25/23.976,
        'NTSC2FILM' : 23.976/24,
        'PAL2FILM' : 25/24,
        'FILM2NTSC' : 24/23.976,
        'FILM2PAL' : 24/25
    }

    TOP_MARKER = '{\\an8}'

    def __init__(self, shift = 0, source_fps = 23.976, scale_factor = 1, subtitle_language = None):
        self.shift = shift
        self.source_fps = source_fps
        self.subtitle_language = subtitle_language
        self.scale_factor = scale_factor
        self.ssa_timestamp_min_sep = 200
        self.use_cosmetic_filter = True
        self.use_language_filter = True

        self._styles = {}
        self._italic_style_ids = []
        self._top_regions_ids = []

        self._allowed_style_attrs = (
            'color',
            'fontStyle',
            'fontWeight',
        )

        ## This variable stores the language ID from the xml file.
        #  But it may not exist or it may be wrong.
        self.lang = None

        self.ssa_style = OrderedDict([('Fontname', 'Arial'), ('Fontsize', 50), \
                          ('PrimaryColour', '&H00EEEEEE'), ('BackColour', '&H40000000'), ('OutlineColour', '&H00000000'), \
                          ('Bold', 0), ('Italic', 0), \
                          ('Alignment', 2), \
                          ('BorderStyle', 1), \
                          ('Outline', 2), ('Shadow', 3), \
                          ('MarginL', 40), ('MarginR', 40), ('MarginV', 40)])
        self.ssa_playresx = 1280
        self.ssa_playresy = 720

        self.entries = []

    def set_video_aspect_ratio(self, ratio):
        """ Adjust the SSA options PlaResX and PlayRexY according to the aspect ratio of the video """
        self.ssa_playresy = int(self.ssa_playresx / ratio)

    def parse_subtitle_file(self, filename):
        """Read and parse a subtitle file.
        If the file has the vtt or srt extension it will be parsed as a vtt. Otherwise it will be parsed as ttml.
        The result is stored in the `entries` list, as begin (ms), end (ms), text, position.
        """

        extension = os.path.splitext(filename)[1].lower()
        if extension == ".srt" or extension == ".vtt":
            ttml.parse_vtt_file(input_file)
        else:
            ttml.parse_ttml_file(input_file)

    def parse_ttml_file(self, filename):
        """Read and parse a ttml/xml/dfxp file.
        The result is stored in the `entries` list, as begin (ms), end (ms), text, position.
        """

        doc = ''
        import io
        with io.open(filename, 'r', encoding='utf-8') as handle:
            doc = handle.read()
        self.parse_ttml_from_string(doc.encode('utf-8'))

    def parse_ttml_from_string(self, doc):
        """Read and parse a ttml/xml/dfxp subtitle from a string.
        The result is stored in the `entries` list, as begin (ms), end (ms), text, position.
        """

        del self.entries [:]
        self._tc = TimestampConverter()

        ttml_dom = minidom.parseString(doc)
        self._encoding = ttml_dom.encoding

        if self._encoding and self._encoding.lower() not in ['utf8', 'utf-8']:
            # Don't bother with subtitles that aren't utf-8 encoded
            # but assume utf-8 when the encoding attr is missing
            raise NotImplementedError('Source is not utf-8 encoded')

        # Get the root tt element (assume the file contains
        # a single subtitle document)
        tt_element = ttml_dom.getElementsByTagNameNS('*', 'tt')[0]

        # Extract doc language
        # https://tools.ietf.org/html/rfc4646#section-2.1
        language_tag = tt_element.getAttribute('xml:lang') or ''
        self.lang = re.split(r'\s+', language_tag.strip())[0].split('-')[0]

        # Store TT parameters as instance vars (in camel case)
        opttime = {}
        for ttp_name, defval, convfn in (
                # (tt param, default val, fn to process the str)
                ('frameRate', 0, lambda x: float(x)),
                ('tickRate', 0, lambda x: int(x)),
                ('timeBase', 'media', lambda x: x),
                ('clockMode', '', lambda x: x),
                ('frameRateMultiplier', 1, lambda x: int(x)),
                ('subFrameRate', 1, lambda x: int(x)),
                ('markerMode', '', lambda x: x),
                ('dropMode', '', lambda x: x),
        ):
            ttp_val = getattr(
                tt_element.attributes.get('ttp:' + ttp_name), 'value', defval)
            opttime[Ttml2Ssa.snake_to_camel(ttp_name)] = convfn(ttp_val)

        if opttime['time_base'] not in Ttml2Ssa.TIME_BASES:
            raise NotImplementedError('No support for "{}" time base'.format(
                opttime['time_base']))

        # Set effective tick rate as per
        # https://www.w3.org/TR/ttml1/#parameter-attribute-tickRate
        # This will obviously only be made use of if we encounter offset-time
        # expressions that have the tick metric.
        self._tc.tick_rate = opttime['tick_rate']
        if not opttime['tick_rate'] and opttime['frame_rate']:
            self._tc.tick_rate = int(opttime['frame_rate'] * opttime['sub_frame_rate'])
        elif not opttime['tick_rate']:
            self._tc.tick_rate = 1

        # Set FPS to source_fps if no TT param
        self._tc.frame_rate = opttime['frame_rate'] or self.source_fps

        # Grab <style>s
        # https://www.w3.org/TR/ttml1/#styling-attribute-vocabulary
        for styles_container in ttml_dom.getElementsByTagName('styling'):
            for style in styles_container.getElementsByTagName('style'):
                style_id = getattr(
                    style.attributes.get('xml:id', {}), 'value', None)
                if not style_id:
                    continue
                self._styles[style_id] = self._get_tt_style_attrs(style, True)
                if self._styles[style_id]['font_style'] == 'italic':
                    self._italic_style_ids.append(style_id)

        # Grab top regions
        for layout_container in ttml_dom.getElementsByTagName('layout'):
            for region in layout_container.getElementsByTagName('region'):
                region_id = getattr(
                    region.attributes.get('xml:id', {}), 'value', None)
                if region_id and region.getAttribute('tts:displayAlign') == 'before':
                    self._top_regions_ids.append(region_id)

        # Get em <p>s.
        #
        # CAUTION: This is very naive and will fail us when the TTML
        # document contains multiple local time contexts with their own
        # offsets, or even just a single context with an offset other
        # than zero.
        lines = [i for i in ttml_dom.getElementsByTagNameNS('*', 'p') \
            if 'begin' in i.attributes.keys()]

        for p in lines:
            entry = {}
            ms_begin, ms_end, text, position = self._process_parag(p)
            entry['ms_begin'] = ms_begin
            entry['ms_end'] = ms_end
            entry['text'] = text
            entry['position'] = position
            self.entries.append(entry)

        self._apply_options()

    def _apply_options(self):
        if self.scale_factor != 1:
            self._scale_timestamps(self.scale_factor)

        if self.shift:
            self._shift_timestamps(self.shift)

        if self.use_cosmetic_filter:
            self._cosmetic_filter()

        if self.use_language_filter:
            self._language_fix_filter()

    def _get_tt_style_attrs(self, node, in_head=False):
        """Extract node's style attributes

        Node can be a style definition element or a content element (<p>).

        Attributes are filtered against :attr:`Ttml2Ssa._allowed_style_attrs`
        and returned as a dict whose keys are attribute names camel cased.
        """

        style = {}
        for attr_name in self._allowed_style_attrs:
            tts = 'tts:' + attr_name
            attr_name = Ttml2Ssa.snake_to_camel(attr_name)
            style[attr_name] = node.getAttribute(tts) or ''
        if not in_head:
            style['style_id'] = node.getAttribute('style')
        return style


    def _extract_dialogue(self, nodes, styles=[]):
        """Extract text content and styling attributes from <p> elements.

        Args:
            nodes (xml.dom.minidom.Node): List of <p> elements
            styles (list): List of style signifiers that should be
                applied to each node

        Return:
            List of SRT paragraphs (strings)
        """

        dialogue = []

        for node in nodes:
            _styles = []

            if node.nodeType == node.TEXT_NODE:
                format_str = '{}'

                # Take the liberty to make a few stylistic choices. We don't
                # want too many leading spaces or any unnecessary new lines
                text = re.sub(r'^\s{4,}', '', node.nodeValue.replace('\n', ''))

                for style in styles:
                    format_str = '{ot}{f}{et}'.format(
                        et='</{}>'.format(style),
                        ot='<{}>'.format(style),
                        f=format_str)

                dialogue.append(format_str.format(text))

            elif node.localName == 'br':
                dialogue.append('\n')

            # Checks for italics for now but shouldn't be too much work to
            # support bold text or colors
            elif node.localName == 'span':
                style_attrs = self._get_tt_style_attrs(node)
                inline_italic = style_attrs['font_style'] == 'italic'
                assoc_italic = style_attrs['style_id'] in self._italic_style_ids
                if inline_italic or assoc_italic or node.parentNode.getAttribute('style') == 'AmazonDefaultStyle':
                    _styles.append('i')

            if node.hasChildNodes():
                dialogue += self._extract_dialogue(node.childNodes, _styles)

        return ''.join(dialogue)

    def _process_parag(self, paragraph):
        """Extract begin and end attrs, and text content of <p> element.

        Args:
            paragragh (xml.dom.minidom.Element): <p> element.

        Returns:
            Tuple containing
                begin in ms,
                end in ms,
                text content in Subrip (SRT) format,
                position (top or bottom) where the text should appear
        """

        begin = paragraph.attributes['begin'].value
        end = paragraph.attributes['end'].value

        ms_begin = self._tc.timeexpr_to_ms(begin)
        ms_end = self._tc.timeexpr_to_ms(end)

        dialogue = self._extract_dialogue(paragraph.childNodes)

        # Trim lines and remove empty lines
        new_text = ""
        for line in dialogue.splitlines():
            line = line.strip()
            if line != "":
                if new_text != "": new_text += "\n"
                new_text += line
        dialogue = new_text

        position = 'top' if paragraph.getAttribute('region') in self._top_regions_ids else 'bottom'

        return ms_begin, ms_end, dialogue, position


    def parse_vtt_file(self, filename):
        """Read and parse a vtt/srt file.
        The result is stored in the `entries` list, as begin (ms), end (ms), text, position.
        """

        vtt = ""
        import io
        with io.open(filename, 'r', encoding='utf-8') as handle:
            vtt = handle.read()
        self.parse_vtt_from_string(vtt)

    def parse_vtt_from_string(self, vtt):
        """Read and parse a vtt/srt subtitle from a string.
        The result is stored in the `entries` list, as begin (ms), end (ms), text, position.
        """

        del self.entries [:]
        self._tc = TimestampConverter()

        lines = vtt.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1
            m = re.match('(?P<t1>\d{2}:\d{2}:\d{2}[\.,]\d{3})\s-->\s(?P<t2>\d{2}:\d{2}:\d{2}[\.,]\d{3})(?:.*(?P<pos>start|end))?', line)
            if m:
                entry = {}
                entry['ms_begin'] = self._tc.timeexpr_to_ms(m.group('t1').replace(',', '.'))
                entry['ms_end'] = self._tc.timeexpr_to_ms(m.group('t2').replace(',', '.'))
                entry['position'] = 'top' if m.group('pos') == 'start' else 'bottom'
                text = ""
                while i < len(lines):
                    line = lines[i].strip()
                    i += 1
                    if line:
                        if text: text += "\n"
                        text += line
                    else:
                        break
                entry['text'] = text
                self.entries.append(entry)
        self._apply_options()

    def generate_srt(self):
        """Return a string with the generated subtitle document in srt format."""

        entries = sorted(self.entries, key=lambda begin: begin['ms_begin'])

        srt_format_str = '{}\r\n{} --> {}\r\n{}\r\n\r\n'
        res = ''
        entry_count = 1
        for entry in entries:
            text = entry['text'].replace("\n", "\r\n")
            if entry['position'] == 'top':
                text = Ttml2Ssa.TOP_MARKER + text
            res += srt_format_str.format(entry_count, \
                                         self._tc.ms_to_subrip(entry['ms_begin']), \
                                         self._tc.ms_to_subrip(entry['ms_end']), \
                                         text)
            entry_count += 1
        return res

    def _paragraphs_to_ssa(self, timestamp_min_sep = 200):
        entries = sorted(self.entries, key=lambda begin: begin['ms_begin'])

        if (timestamp_min_sep > 0 and len(self.entries) > 1):
            for i in range(len(entries)):
                if i == 0: continue
                diff =  entries[i]['ms_begin'] - entries[i-1]['ms_end']
                if (diff < timestamp_min_sep):
                    s = round((timestamp_min_sep - diff) / 2)
                    entries[i]['ms_begin'] += s
                    entries[i-1]['ms_end'] -= s

        ssa_format_str = 'Dialogue: 0,{},{},Default,{}\r\n'
        res = ""
        for entry in entries:
            text = entry['text']
            text = text.replace("\n", "\\N").replace("<i>", "{\i1}").replace("</i>", "{\i0}")
            if entry['position'] == 'top':
                text = Ttml2Ssa.TOP_MARKER + text
            res += ssa_format_str.format(self._tc.ms_to_ssa(entry['ms_begin']), self._tc.ms_to_ssa(entry['ms_end']), text)
        return res

    def generate_ssa(self):
        """Return a string with the generated subtitle document in ssa format."""

        res = "[Script Info]\r\n" \
            "ScriptType: v4.00+\r\n" \
            "Collisions: Normal\r\n" \
            "PlayDepth: 0\r\n" \
            "PlayResX: {}\r\n" \
            "PlayResY: {}\r\n\r\n" \
            "[V4+ Styles]\r\n" \
            "Format: Name, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\r\n" \
            "Style: Default,{},{},{},{},{},{},{},{},{},{},{},{},{},{}\r\n\r\n" \
            "[Events]\r\n" \
            "Format: Layer, Start, End, Style, Text\r\n" \
            .format(self.ssa_playresx, self.ssa_playresy, \
                    *list(self.ssa_style.keys()) + list(self.ssa_style.values()))

        res += self._paragraphs_to_ssa(self.ssa_timestamp_min_sep)
        return res

    def _shift_timestamps(self, milliseconds):
        self._printinfo("Shifting {} milliseconds".format(milliseconds))
        for entry in self.entries:
            entry['ms_begin'] += milliseconds;
            entry['ms_end'] += milliseconds;

    def _scale_timestamps(self, multiplier):
        self._printinfo("Scale factor: {}".format(multiplier))
        for entry in self.entries:
            entry['ms_begin'] *= multiplier;
            entry['ms_end'] *= multiplier;

    def _cosmetic_filter(self):
        total_count = 0
        for entry in self.entries:
            entry['text'], n_changes = re.subn('—', '-', entry['text']);
            total_count += n_changes
            entry['text'], n_changes = re.subn(r'^(<i>|</i>|)-(\S)', r'\1- \2', entry['text'], flags=re.MULTILINE)
            total_count += n_changes
        self._printinfo("Cosmetic changes: {}".format(total_count))

    def _language_fix_filter(self):
        lang = self.subtitle_language if self.subtitle_language else self.lang
        es_replacements = [('\xA8', '¿'), ('\xAD', '¡'), ('ń', 'ñ')]
        total_count = 0
        for entry in self.entries:
            if lang == 'es':
                for rep in es_replacements:
                    total_count +=  entry['text'].count(rep[0])
                    entry['text'] = entry['text'].replace(rep[0], rep[1])
            if lang == 'ar':
                from unicodedata import lookup
                entry['text'], n_changes = re.subn(r'^(?!{}|{})'.format(lookup('RIGHT-TO-LEFT MARK'), lookup('RIGHT-TO-LEFT EMBEDDING')),
                                              lookup('RIGHT-TO-LEFT EMBEDDING'), entry['text'], flags=re.MULTILINE)
                total_count += n_changes
                total_count += entry['text'].count('?')
                total_count += entry['text'].count(',')
                entry['text'] = entry['text'].replace('?', '؟').replace(',', '،')
        self._printinfo("Replacements for language '{}': {}".format(lang, total_count))

    def _printinfo(self, text):
        print(text)

    def write2file(self, output):
        """Write subtitle to file

        It will be saved as ssa if the output filename
        extension is ssa or ass. As srt otherwise.
        """

        extension = os.path.splitext(output)[1].lower()

        import io
        with io.open(output, 'w', encoding='utf-8-sig') as handle:
            if (extension == '.ssa' or extension == '.ass'):
                handle.write(self.generate_ssa())
            else:
                handle.write(self.generate_srt())

    @staticmethod
    def mfn2subfn(media_filename, lang=None, m_ext=True, format='srt'):
        """Create subtitle filename from media filename
        """

        extension = 'ssa' if format == 'ssa' else 'srt'

        if not m_ext:
            return '{}{}.{}'.format(
                media_filename,
                '.{}'.format(lang) if lang else '', extension)
        else:
            return '{}{}.{}'.format(
                '.'.join(media_filename.split('.')[:-1]),
                '.{}'.format(lang) if lang else '', extension)

    @staticmethod
    def mfn2srtfn(media_filename, lang=None, m_ext=True):
        """Create SRT filename from media filename

        Uses the <media file w/o ext>.<lang>.srt form recognized by Plex,
        Kodi, VLC, MPV, and others.
        """

        return Ttml2Ssa.mfn2subfn(media_filename, lang, m_ext, 'srt')

    @staticmethod
    def snake_to_camel(s):
        camel = ''
        for c in s:
            d = ord(c)
            if d < 91 and d > 64:
                camel += '_' + c.lower()
            else:
                camel += c
        return camel


class Ttml2SsaKodi(Ttml2Ssa):
    def __init__(self, shift = 0, source_fps = 23.976, scale_factor = 1, subtitle_language = None):
        super(Ttml2SsaKodi, self).__init__(shift, source_fps, scale_factor, subtitle_language)
        import xbmcaddon
        self.addon = xbmcaddon.Addon('script.module.ttml2ssa')
        self.ssa_style["Fontname"] = self.addon.getSetting('fontname')
        self.ssa_style["Fontsize"] = self.addon.getSettingInt('fontsize')
        self.ssa_style["PrimaryColour"] = "&H" + self.addon.getSetting('primarycolor')
        self.ssa_style["BackColour"] = "&H" + self.addon.getSetting('backcolor')
        self.ssa_style["OutlineColour"] = "&H" + self.addon.getSetting('outlinecolor')
        self.ssa_style["BorderStyle"] = 1 if self.addon.getSettingInt('borderstyle') == 0 else 3
        self.ssa_style["Outline"] = self.addon.getSettingInt('outline')
        self.ssa_style["Shadow"] = self.addon.getSettingInt('shadow')
        self.ssa_style["Bold"] = -1 if self.addon.getSettingBool('bold') else 0
        self.ssa_style["Italic"] = -1 if self.addon.getSettingBool('italic') else 0
        self.ssa_style["MarginL"] = self.addon.getSettingInt('marginl')
        self.ssa_style["MarginR"] = self.addon.getSettingInt('marginr')
        self.ssa_style["MarginV"] = self.addon.getSettingInt('marginv')
        self.use_cosmetic_filter = self.addon.getSettingBool('cosmetic_filter')
        self.use_language_filter = self.addon.getSettingBool('language_filter')
        self.ssa_timestamp_min_sep = self.addon.getSettingInt('min_sep')
        self._printinfo("SSA style: {}".format(self.ssa_style))
        self._printinfo("Cosmetic filter: {}".format("enabled" if self.use_cosmetic_filter else "disabled"))
        self._printinfo("Language filter: {}".format("enabled" if self.use_language_filter else "disabled"))
        self._printinfo("Timestamp minimum separation: {}".format(self.ssa_timestamp_min_sep))

    def _printinfo(self, text):
        import xbmc
        xbmc.log("Ttml2Ssa: {}".format(text), xbmc.LOGINFO)


if __name__ == '__main__':

    import argparse

    argparser = argparse.ArgumentParser(
        description='Convert TTML/XML/DFXP subtitles to SubRip (SRT) or SSA/ASS format.')
    argparser.add_argument('input-file',
        nargs="?",
        help='subtitle file',
        action='store')
    argparser.add_argument('output-file',
        nargs='?',
        help='output file with extension srt, ssa or ass',
        action='store')
    argparser.add_argument('-s', '--shift',
        dest='shift', help='shift',
        metavar='ms', nargs='?',
        const=0, default=0, type=float,
        action='store')
    argparser.add_argument('-f', '--fps',
        dest='sfps', metavar='fps',
        help='frames per second (default: 23.976)',
        nargs='?', const=23.976,
        default=23.976, type=float,
        action='store')
    argparser.add_argument('-sf', '--scale-factor',
        dest='scale', metavar='number or label',
        help='multiplies the timestamps by this mumber. You can use also any of these labels: '
             'NTSC2PAL (23.976/25), PAL2NTSC (25/23.976), '
             'NTSC2FILM (23.976/24), PAL2FILM (25/24), '
             'FILM2NTSC (24/23.976), FILM2PAL (24/25)',
        nargs='?', type=str, default='1', action='store')
    argparser.add_argument('--min-sep-ms',
        dest="ssa_timestamp_min_sep", metavar="ms",
        help="minimum separation (in ms) between framestamps (SSA/ASS only)",
        nargs="?", type=int, default=200, action='store')
    argparser.add_argument('-l', '--lang',
        dest="lang", metavar="language code",
        help="subtitle language code ('en', 'es', etc,). Used with the language filter",
        nargs="?", type=str, default=None, action='store')
    argparser.add_argument('-ncf', '--no-cosmetic-filter',
        dest="cosmetic_filter",
        help="disables a filter which makes some cosmetic changes, like adding a space after the symbol '-' and the next word",
        action='store_false')
    argparser.add_argument('-nlf', '--no-language-filter',
        dest="language_filter",
        help="disables a filter which may fix some wrong characters in some specific languages",
        action='store_false')
    argparser.add_argument('-v', '--version',
        dest="version",
        help="displays the version of this application",
        action='store_true')
    args = argparser.parse_args()

    if args.scale in Ttml2Ssa.SCALE.keys():
        scale_factor = Ttml2Ssa.SCALE[args.scale]
    else:
        scale_factor = eval(args.scale)

    ttml = Ttml2Ssa(shift=args.shift, source_fps = args.sfps, scale_factor = scale_factor, subtitle_language = args.lang)
    ttml.ssa_timestamp_min_sep = args.ssa_timestamp_min_sep
    ttml.use_cosmetic_filter = args.cosmetic_filter
    ttml.use_language_filter = args.language_filter

    if args.version:
        print("ttml2ssa version {}".format(ttml.VERSION))

    input_file = getattr(args, 'input-file')
    output_file = getattr(args, 'output-file')

    if input_file:
        ttml.parse_subtitle_file(input_file)
        if output_file:
            ttml.write2file(output_file)
