#Makefile wrapper for the python installation

default: all

install:
	#Install the python data
	/usr/bin/env python setup.py install --root=$(DESTDIR)

	#Install our glade layout
	-mkdir -p $(DESTDIR)/usr/share/greg-tic-tac-toe/glade
	-cp board.glade $(DESTDIR)/usr/share/greg-tic-tac-toe/glade

	
all:




