## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = src 

geineddocdir = ${prefix}/doc/geined
geineddoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(geineddoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(geineddocdir)
