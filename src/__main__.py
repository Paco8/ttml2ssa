# encoding: utf-8
#
#  --------------------------------------------
#  based on https://github.com/yuppity/ttml2srt
#  --------------------------------------------
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import unicode_literals, absolute_import, division
from ttml2ssa import Ttml2Ssa

if __name__ == '__main__':

    import argparse

    argparser = argparse.ArgumentParser(
        description='Convert TTML/XML/DFXP/SRT/VTT subtitles to SubRip (SRT), SSA/ASS or WEBVTT (VTT) format.')
    argparser.add_argument('input-files',
        nargs="*",
        help='subtitle files',
        action='store')
    argparser.add_argument('-o', '--output',
        dest='output-file', metavar="output file",
        nargs='?',
        help='output file with extension srt, ssa or ass',
        action='store')
    argparser.add_argument('-v', '--version',
        dest="version",
        help="displays the version of this application and exits",
        action='store_true')
    argparser.add_argument('--shift',
        dest='shift',
        help='increases all timestamps by the specified value. You can use a negative number',
        metavar='ms', nargs='?',
        const=0, default=0, type=float,
        action='store')
    """
    argparser.add_argument('-f', '--fps',
        dest='sfps', metavar='fps',
        help='frames per second (default: 23.976)',
        nargs='?', const=23.976,
        default=23.976, type=float,
        action='store')
    """
    argparser.add_argument('--scale-factor',
        dest='scale', metavar='number or label',
        help='multiplies the timestamps by this mumber. You can use also any of these labels: '
             'NTSC2PAL (23.976/25), PAL2NTSC (25/23.976), '
             'NTSC2FILM (23.976/24), PAL2FILM (25/24), '
             'FILM2NTSC (24/23.976), FILM2PAL (24/25)',
        nargs='?', type=str, default='1', action='store')
    argparser.add_argument('-l', '--lang',
        dest="lang", metavar="language code",
        help="subtitle language code ('en', 'es', etc,). It's used by the language filter",
        nargs="?", type=str, default=None, action='store')
    argparser.add_argument('-a', '--video-aspect',
        dest='aspect', metavar='number',
        help='the aspect ratio of the video. '
             'It\'s used to calculate the correct PlayResY and PlayResY options for the SSA style. '
             'Default: 16/9',
        nargs='?', type=str, default='16/9', action='store')
    argparser.add_argument('--no-cosmetic-fix',
        dest="cosmetic_fix",
        help="disables a filter which makes some cosmetic changes, like adding a space after the symbol '-' and the next word",
        action='store_false')
    argparser.add_argument('--no-language-fix',
        dest="language_fix",
        help="disables a filter which can fix some wrong characters in some specific languages",
        action='store_false')
    argparser.add_argument('--no-fix-amazon-errors',
        dest="fix_amazon",
        help="don't try to fix errors that may occur in subtitles from Amazon",
        action='store_false')
    argparser.add_argument('-c', '--charset',
        dest='encoding', metavar='encoding',
        help='the encoding of the input file',
        nargs='?',
        default=None, type=str,
        action='store')
    argparser.add_argument('--output-format',
        dest='output_format', metavar="srt, ssa or vtt",
        nargs='?',
        help='output format to use if an output file has not been set',
        default='ssa', choices=['srt', 'ssa', 'vtt'],
        action='store')
    argparser.add_argument('-srt', '--srt',
        dest='output_format',
        help='equivalent to --output_format srt',
        const='srt',
        action='store_const')
    argparser.add_argument('-vtt', '--vtt',
        dest='output_format',
        help='equivalent to --output_format vtt',
        const='vtt',
        action='store_const')
    argparser.add_argument('--no-italics',
        dest='allow_italics',
        help='removes the italic tags from the dialog texts',
        action='store_false')
    argparser.add_argument('--no-top',
        dest='allow_top_pos',
        help='all dialog will be displayed at the bottom of the screen',
        action='store_false')

    argparser.add_argument('--ssa-fontname', '-f',
        dest='fontname', metavar='font',
        help='the font name (default: arial)',
        nargs='?',
        default='Arial', type=str,
        action='store')
    argparser.add_argument('--ssa-fontsize', '-fs',
        dest='fontsize', metavar='number',
        help='the font size (default: 50)',
        nargs='?',
        default=50, type=int,
        action='store')
    argparser.add_argument('--ssa-primary-color', '-pc',
        dest='primary_color', metavar='color',
        help='the primary color in format AABBGGRR or color name (default: white)',
        nargs='?',
        default='white', type=str,
        action='store')
    argparser.add_argument('--ssa-back-color', '-bc',
        dest='back_color', metavar='color',
        help='the back color in format AABBGGRR or color name (default: 40000000)',
        nargs='?',
        default='40000000', type=str,
        action='store')
    argparser.add_argument('--ssa-outline-color', '-oc',
        dest='outline_color', metavar='color',
        help='the outline color in format AABBGGRR or color name (default: black)',
        nargs='?',
        default='black', type=str,
        action='store')
    argparser.add_argument('--ssa-bold', '-b',
        dest='ssa_bold',
        help='the font will be in bold',
        action='store_true')
    argparser.add_argument('--ssa-italic', '-i',
        dest='ssa_italic',
        help='the font will be in italic',
        action='store_true')

    argparser.add_argument('--no-timestamp-manipulation',
        dest="timestamp_manipulation",
        help="no changes will be made on timestamps",
        action='store_false')
    argparser.add_argument('--no-fix-collisions',
        dest="fix_collisions",
        help="collisions on timestamps won't be fixed",
        action='store_false')   
    argparser.add_argument('--min-sep-ms',
        dest="ssa_timestamp_min_sep", metavar="ms",
        help="minimum separation (in ms) between framestamps (SSA/ASS output only)",
        nargs="?", type=int, default=200, action='store')

    args = argparser.parse_args()

    if args.scale in Ttml2Ssa.SCALE.keys():
        scale_factor = Ttml2Ssa.SCALE[args.scale]
    else:
        scale_factor = eval(args.scale)

    ttml = Ttml2Ssa(shift=args.shift, scale_factor=scale_factor, subtitle_language=args.lang)
    #ttml.source_fps = args.sfps
    ttml.use_cosmetic_filter = args.cosmetic_fix
    ttml.use_language_filter = args.language_fix
    ttml.fix_amazon_errors = args.fix_amazon
    ttml.allow_italics = args.allow_italics
    ttml.allow_top_pos = args.allow_top_pos
    ttml.allow_timestamp_manipulation = args.timestamp_manipulation
    ttml.fix_timestamp_collisions = args.fix_collisions
    ttml.ssa_timestamp_min_sep = args.ssa_timestamp_min_sep
    ttml.set_video_aspect_ratio(eval(args.aspect))

    ttml.ssa_style["Fontname"] = args.fontname
    ttml.ssa_style["Fontsize"] = args.fontsize
    ttml.ssa_style["PrimaryColour"] = ttml.string_to_color(args.primary_color)
    ttml.ssa_style["BackColour"] = ttml.string_to_color(args.back_color)
    ttml.ssa_style["OutlineColour"] = ttml.string_to_color(args.outline_color)
    ttml.ssa_style["Bold"] = -1 if args.ssa_bold else 0
    ttml.ssa_style["Italic"] = -1 if args.ssa_italic else 0

    if args.version:
        print("ttml2ssa version {}".format(ttml.VERSION))
        quit()

    input_files = getattr(args, 'input-files')
    output_file = getattr(args, 'output-file')

    if output_file and len(input_files) > 1:
        del input_files[1:]

    if not input_files:
        argparser.print_usage()

    for input_file in input_files:
        if output_file:
            output = output_file
        else:
            import os.path
            basename = os.path.splitext(input_file)[0]
            output = basename + "." + args.output_format
        print("Converting {} to {}".format(input_file, output))
        ttml.parse_subtitle_file(input_file, args.encoding)
        ttml.write2file(output)
