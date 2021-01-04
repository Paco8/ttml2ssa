all: es.po en.po

empty.pot: Makefile create_pot.php
	./create_pot.php > empty.pot

en.po: empty.pot
	msgmerge --lang=en -U -N --backup=numbered en.po empty.pot

es.po: empty.pot
	msgmerge --lang=es -U -N --backup=numbered es.po empty.pot

clean:
	-rm empty.pot
	-rm *~
