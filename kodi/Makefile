VERSION = $(shell sed -n -e "s/.*VERSION = '\(.*\)'/\1/p" ../src/ttml2ssa.py)
OUTPUT_DIR = script.module.ttml2ssa

install: ../src/ttml2ssa.py ../src/timestampconverter.py addon.xml-k18 addon.xml-k19
	-install -d $(OUTPUT_DIR)/resources/lib/
	install -m 644 ../src/ttml2ssa.py $(OUTPUT_DIR)/resources/lib/
	install -m 644 ../src/timestampconverter.py $(OUTPUT_DIR)/resources/lib/
	install -m 644 addon.xml-k18 $(OUTPUT_DIR)/
	install -m 644 addon.xml-k19 $(OUTPUT_DIR)/
	install -m 644 default.py $(OUTPUT_DIR)/
	install -m 644 icon.png $(OUTPUT_DIR)/
	install -m 644 settings.xml-k18 $(OUTPUT_DIR)/resources/
	install -m 644 settings.xml-k19 $(OUTPUT_DIR)/resources/
	install -m 644 *.jpg $(OUTPUT_DIR)/resources/
	sed -e 's/{version}/$(VERSION)/' -i $(OUTPUT_DIR)/addon.xml-k18
	cp $(OUTPUT_DIR)/addon.xml-k18 $(OUTPUT_DIR)/addon.xml
	cp $(OUTPUT_DIR)/resources/settings.xml-k18 $(OUTPUT_DIR)/resources/settings.xml

	cd translations && make
	-install -d $(OUTPUT_DIR)/resources/language/resource.language.en_gb/
	-install -d $(OUTPUT_DIR)/resources/language/resource.language.es_es/
	-install -d $(OUTPUT_DIR)/resources/language/resource.language.pl_pl/
        -install -d $(OUTPUT_DIR)/resources/language/resource.language.hu_hu/
	install -m 644 translations/en.po $(OUTPUT_DIR)/resources/language/resource.language.en_gb/strings.po
	install -m 644 translations/es.po $(OUTPUT_DIR)/resources/language/resource.language.es_es/strings.po
	install -m 644 translations/pl.po $(OUTPUT_DIR)/resources/language/resource.language.pl_pl/strings.po
	install -m 644 translations/hu.po $(OUTPUT_DIR)/resources/language/resource.language.hu_hu/strings.po

	zip -9 -r script.module.ttml2ssa-$(VERSION)-leia.zip $(OUTPUT_DIR)/ -x \*k18 \*k19
	cp $(OUTPUT_DIR)/addon.xml-k19 $(OUTPUT_DIR)/addon.xml
	sed -e 's/{version}/$(VERSION)/' -i $(OUTPUT_DIR)/addon.xml
	cp $(OUTPUT_DIR)/resources/settings.xml-k19 $(OUTPUT_DIR)/resources/settings.xml
	zip -9 -r script.module.ttml2ssa-$(VERSION)-matrix.zip $(OUTPUT_DIR)/ -x \*k18 \*k19

clean:
	-rm -r $(OUTPUT_DIR)
	-rm script.module.ttml2ssa-*.zip
	cd translations && make clean
