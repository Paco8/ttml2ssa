# ttml2ssa
Convert TTML/XML/DFXP/VTT/SRT subtitles used by Netflix, HBO, Disney+, Prime Video and others to SRT or SSA/ASS format.

Note: `ttml2ssa` is *not* a full-featured TTML-to-SRT converter and only works on a small subset of TTML documents. Namely, documents that follow the formats seen on the aforementioned streaming services.

## Usage
```
positional arguments:
  input-file            subtitle file
  output-file           output file with extension srt, ssa or ass

optional arguments:
  -h, --help            show this help message and exit
  -s [ms], --shift [ms]
                        shift
  -f [fps], --fps [fps]
                        frames per second (default: 23.976)
  -sf [number or label], --scale-factor [number or label]
                        multiplies the timestamps by this mumber. You can use
                        also any of these labels: NTSC2PAL (23.976/25),
                        PAL2NTSC (25/23.976), NTSC2FILM (23.976/24), PAL2FILM
                        (25/24), FILM2NTSC (24/23.976), FILM2PAL (24/25)
  --min-sep-ms [ms]     minimum separation (in ms) between framestamps
                        (SSA/ASS only)
  -l [language code], --lang [language code]
                        subtitle language code ('en', 'es', etc,). Used with
                        the language filter
  -a [number], --video-aspect [number]
                        the aspect ratio of the video. It's used to calculate
                        the correct PlayResY and PlayResY options for the SSA
                        style. Default: 16/9
  -ncf, --no-cosmetic-filter
                        disables a filter which makes some cosmetic changes,
                        like adding a space after the symbol '-' and the next
                        word
  -nlf, --no-language-filter
                        disables a filter which may fix some wrong characters
                        in some specific languages
  --encoding [ENCODING]
                        the encoding of the input file
  -v, --version         displays the version of this application
```

### Common use cases

Simple conversion:
```
./ttml2ssa.py subtitle_from_netflix.xml subtitle.ssa
```
or
```
./ttml2ssa.py subtitle_from_netflix.xml subtitle.srt
```

Shift everything forward by 2 secs:
```
./ttml2ssa.py -s 2000 subtitle_from_netflix.xml subtitle.srt
```

Convert from one frame rate to another:
```
./ttml2ssa.py -sf 23.976/25 subtitle_from_netflix.xml subtitle.srt
```
or
```
./ttml2ssa.py -sf NTSC2PAL subtitle_from_netflix.xml subtitle.srt
```

Those examples will convert a subtitle made for a movie at 23.976 frames per second for a version sped up to 25 fps (very common in Europe).

### Library
ttml2ssa.py can also be used as a library for other applications.

Simple example:
```
from ttml2ssa import Ttml2Ssa

input_file = 'subtitle.xml'
ttml = Ttml2Ssa()
ttml.parse_subtitle_file(input_file)
ttml.write2file('output.srt') # Saves as SRT
ttml.write2file('output.ssa') # Saves as SSA
```
Without loading or writing files:
```
from ttml2ssa import Ttml2Ssa

ttml_document = 'THIS STRING SHOULD CONTAIN AN XML SUBTITLE DOCUMENT'
ttml = Ttml2Ssa()
ttml.parse_ttml_from_string(ttml_document)
result = ttml.generate_srt()
# or
result = ttml.generate_ssa()
```

### Addon for Kodi
There's also an addon for Kodi
([script.module.ttml2ssa](https://github.com/Paco8/kodi-repo/blob/master/packages/script.module.ttml2ssa/script.module.ttml2ssa-0.1.7.zip)),
which other addons can use to convert subtitles to SRT or SSA.
It provides a configuration dialog where the user can configure the SSA style and other stuff.

You can use it with something like this:
```
from ttml2ssa import Ttml2SsaKodi
...

ttml = Ttml2SsaKodi()
ttml.parse_subtitle_file(input_file)
# or
ttml.parse_ttml_from_string(subtitle_in_a_string)

ttml.write2file('output.srt')
# or
ttml.write2file('output.ssa')

# or
result = ttml.generate_srt()
# or
result = ttml.generate_ssa()
```

To open the ttml2ssa configuration dialog, you can add this to your addon settings.xml:
```
<setting label="SSA Settings" type="action" id="ssa_settings" option="close" action="Addon.OpenSettings(script.module.ttml2ssa)"/>
```

### Authors
ttml2ssa.py by Paco8, based on [ttml2srt](https://github.com/yuppity/ttml2srt) by yuppity.
License: GPL-2.0
