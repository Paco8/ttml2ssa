Ttml2ssa is a library for Kodi which can help you provide better looking
subtitles for your addons.

Even though Kodi is a great software it allows very little customization
of subtitles (SRT format), you can mainly only change the color, that's all.
Subtitles usually look better on other media players.

However Kodi also supports subtitles in SSA/ASS format, which are more
customizable, for example you can add a shadow, set an outline color...
It's also possible to place the subtitles on the top of the screen.

Ttml2ssa is a library that can convert TTML/XML/DFXP/VTT/SRT subtitles used
by Netflix, HBO, Disney+, Prime Video and other stream services to the SSA/ASS
format (it can also convert to SRT and VTT). It provides a configuration dialog
where the user can select the font size, colors, shadow and many other things.
This configuration is shared by all addons that use the ttml2ssa library, so
the user only has set up his preferences in one place.

Another benefit: subtitles will be displayed on top of the screen when
necessary (just like the official apps of Netflix, Disney+ and others
do).

Ttml2ssa can also perform some cosmetic changes so the subtitles look with
the same style among different services.

Using the library is quite easy, it only requires a few lines of code to
convert and save a subtitle.

There's available a repo with modified versions of the Netflix, Amazon, Disney+ and
hbogoeu (only Nordic/Spain) addons with support for ttml2ssa:
https://github.com/Paco8/kodi-repo

More info:
https://github.com/Paco8/ttml2ssa
