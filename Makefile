VERSION = $(shell sed -n -e "s/.*VERSION = '\(.*\)'/\1/p" src/ttml2ssa.py)
PACKAGE-NAME = ttml2ssa-$(VERSION).zip

all: ttml2ssa $(PACKAGE-NAME)

ttml2ssa: Makefile src/timestampconverter.py src/ttml2ssa.py src/__main__.py
	cd src && zip -9 ../app.zip *.py && cd ..
	echo '#!/usr/bin/env python' | cat - app.zip > ttml2ssa
	chmod 755 ttml2ssa
	rm app.zip

$(PACKAGE-NAME): ttml2ssa
	zip -9 $(PACKAGE-NAME) ttml2ssa README.md LICENSE

clean:
	-rm ttml2ssa
	-rm ttml2ssa-*.zip
