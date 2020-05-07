LIBEXECDIR=/usr/local/libexec
SYSCONFDIR=/usr/local/etc
UNITDIR=/etc/systemd/system
PRESETDIR=/etc/systemd/system
PROGNAME=wol-monitor
DESTDIR=

all: src/wol-monitor.service

src/wol-monitor.service: src/wol-monitor.service.in
	cd $(ROOT_DIR) && \
	cat $< | \
	sed "s|@LIBEXECDIR@|$(LIBEXECDIR)|" | \
	sed "s|@SYSCONFDIR@|$(SYSCONFDIR)|" \
	> $@

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: clean dist rpm srpm install

clean:
	cd $(ROOT_DIR) || exit $$? ; rm -f src/*.service
	cd $(ROOT_DIR) || exit $$? ; find -name '*.pyc' -o -name '*~' -print0 | xargs -0 rm -f
	cd $(ROOT_DIR) || exit $$? ; rm -rf *.tar.gz *.rpm
	cd $(ROOT_DIR) || exit $$? ; rm -rf *.egg-info build

dist: clean
	@which rpmspec || { echo 'rpmspec is not available.  Please install the rpm-build package with the command `dnf install rpm-build` to continue, then rerun this step.' ; exit 1 ; }
	cd $(ROOT_DIR) || exit $$? ; excludefrom= ; test -f .gitignore && excludefrom=--exclude-from=.gitignore ; DIR=`rpmspec -q --queryformat '%{name}-%{version}\n' *spec | head -1` && FILENAME="$$DIR.tar.gz" && tar cvzf "$$FILENAME" --exclude="$$FILENAME" --exclude=.git --exclude=.gitignore $$excludefrom --transform="s|^|$$DIR/|" --show-transformed *

srpm: dist
	@which rpmbuild || { echo 'rpmbuild is not available.  Please install the rpm-build package with the command `dnf install rpm-build` to continue, then rerun this step.' ; exit 1 ; }
	cd $(ROOT_DIR) || exit $$? ; rpmbuild --define "_srcrpmdir ." -ts `rpmspec -q --queryformat '%{name}-%{version}.tar.gz\n' *spec | head -1`

rpm: dist
	@which rpmbuild || { echo 'rpmbuild is not available.  Please install the rpm-build package with the command `dnf install rpm-build` to continue, then rerun this step.' ; exit 1 ; }
	cd $(ROOT_DIR) || exit $$? ; rpmbuild --define "_srcrpmdir ." --define "_rpmdir builddir.rpm" -ta `rpmspec -q --queryformat '%{name}-%{version}.tar.gz\n' *spec | head -1`
	cd $(ROOT_DIR) ; mv -f builddir.rpm/*/* . && rm -rf builddir.rpm

install: all
	install -Dm 755 src/$(PROGNAME) -t $(DESTDIR)/$(LIBEXECDIR)/
	install -Dm 644 src/$(PROGNAME).service -t $(DESTDIR)/$(UNITDIR)/
	mkdir -p $(DESTDIR)/$(PRESETDIR)/
	echo 'enable $(PROGNAME).service' > $(DESTDIR)/$(PRESETDIR)/75-$(PROGNAME).preset
