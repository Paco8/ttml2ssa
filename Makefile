ttml2ssa: Makefile src/timestampconverter.py src/ttml2ssa.py src/__main__.py
	cd src && zip -9 ../app.zip *.py && cd ..
	echo '#!/usr/bin/env python' | cat - app.zip > ttml2ssa
	chmod 755 ttml2ssa
	rm app.zip

clean:
	-rm ttml2ssa
