SPEC := $(notdir $(CURDIR)).spec

RPMBUILD := rpmbuild
RPMBUILD_ARGS := --define "_sourcedir $(CURDIR)" --define "_rpmdir $(CURDIR)" --define "_srcrpmdir $(CURDIR)" --define "dist .el9"

.PHONY: srpm rpm getsource
getsource: $(SPEC)
	spectool -g $<

srpm: $(SPEC) getsource
	$(RPMBUILD) $(RPMBUILD_ARGS) -bs $<

rpm: $(SPEC) getsource
	$(RPMBUILD) $(RPMBUILD_ARGS) -bb $<
