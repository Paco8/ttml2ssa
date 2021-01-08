# encoding: utf-8
#
#  --------------------------------------------
#  based on https://github.com/yuppity/ttml2srt
#  --------------------------------------------
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals, absolute_import, division
from ttml2ssa import Ttml2Ssa

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
    argparser.add_argument('-a', '--video-aspect',
        dest='aspect', metavar='number',
        help='the aspect ratio of the video. '
             'It\'s used to calculate the correct PlayResY and PlayResY options for the SSA style. '
             'Default: 16/9',
        nargs='?', type=str, default='16/9', action='store')
    argparser.add_argument('-ncf', '--no-cosmetic-filter',
        dest="cosmetic_filter",
        help="disables a filter which makes some cosmetic changes, like adding a space after the symbol '-' and the next word",
        action='store_false')
    argparser.add_argument('-nlf', '--no-language-filter',
        dest="language_filter",
        help="disables a filter which may fix some wrong characters in some specific languages",
        action='store_false')
    argparser.add_argument('-c', '--charset',
        dest='encoding', metavar='encoding',
        help='the encoding of the input file',
        nargs='?',
        const=0, default=None, type=str,
        action='store')
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
    ttml.set_video_aspect_ratio(eval(args.aspect));

    if args.version:
        print("ttml2ssa version {}".format(ttml.VERSION))

    input_file = getattr(args, 'input-file')
    output_file = getattr(args, 'output-file')

    if not input_file:
        argparser.print_usage()

    if input_file:
        ttml.parse_subtitle_file(input_file, args.encoding)
        if output_file:
            ttml.write2file(output_file)
