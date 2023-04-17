all: es.po en.po pl.po

empty.pot: Makefile create_pot.php
	./create_pot.php > empty.pot

en.po: empty.pot
	msgmerge --lang=en -U -N --backup=numbered en.po empty.pot

es.po: empty.pot
	msgmerge --lang=es -U -N --backup=numbered es.po empty.pot

pl.po: empty.pot
	msgmerge --lang=pl -U -N --backup=numbered pl.po empty.pot
	
pl.po: empty.pot
	msgmerge --lang=pl -U -N --backup=numbered hu.po empty.pot

clean:
	-rm empty.pot
	-rm *~
