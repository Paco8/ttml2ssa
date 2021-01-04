
VERSION=0.1.7
PYTHON_VERSION=2.26.0

OUTPUT_DIR=script.module.ttml2ssa

install: ../ttml2ssa.py addon.xml-k18 addon.xml-k19
	-install -d $(OUTPUT_DIR)/resources/lib/
	install -m 644 ../ttml2ssa.py $(OUTPUT_DIR)/resources/lib/
	install -m 644 addon.xml-k18 $(OUTPUT_DIR)/
	install -m 644 addon.xml-k19 $(OUTPUT_DIR)/
	install -m 644 icon.png $(OUTPUT_DIR)/
	install -m 644 settings.xml $(OUTPUT_DIR)/resources/
	sed -e 's/{version}/$(VERSION)/' -i $(OUTPUT_DIR)/addon.xml-k18
	#sed -e 's/{PYTHON_VERSION}/$(PYTHON_VERSION)/' -i $(OUTPUT_DIR)/addon.xml

	cd translations && make
	-install -d $(OUTPUT_DIR)/resources/language/resource.language.en_gb/
	-install -d $(OUTPUT_DIR)/resources/language/resource.language.es_es/
	install -m 644 translations/en.po $(OUTPUT_DIR)/resources/language/resource.language.en_gb/strings.po
	install -m 644 translations/es.po $(OUTPUT_DIR)/resources/language/resource.language.es_es/strings.po

	#zip -9 -r script.module.ttml2ssa-$(VERSION).zip $(OUTPUT_DIR)/

clean:
	-rm -r $(OUTPUT_DIR)
	cd translations && make clean
