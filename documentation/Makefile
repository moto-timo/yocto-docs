# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: Makefile publish transition

ALLVERS:= $(dir $(wildcard $(SOURCEDIR)/transition/*/index.rst))
ALLVERS:= $(subst ./transition/,,$(ALLVERS))
ALLVERS:= $(subst /,,$(ALLVERS))

transition:
	for ver in $(ALLVERS) ; do \
		$(SPHINXBUILD) -M html "$(SOURCEDIR)"/transition/$$ver/ "$(BUILDDIR)"/$$ver $(SPHINXOPTS) $(O) -c "$(SOURCEDIR)"  ;\
	done

publish: transition
	rm -rf $(BUILDDIR)/final/
	mkdir -p $(BUILDDIR)/final/
	for ver in $(ALLVERS) ; do \
		mkdir -p $(BUILDDIR)/final/$$ver ;\
		cp -r $(BUILDDIR)/$$ver/html/* $(BUILDDIR)/final/$$ver/ ;\
	done
