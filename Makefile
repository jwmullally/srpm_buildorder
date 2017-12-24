PKG=python-srpm_buildorder
VER=0.1

all: rpm

test:
	python3 setup.py nosetests

srpm: clean
	mkdir -p rpmbuild/SOURCES
	tar --exclude-vcs --exclude='./rpmbuild' --transform "s;^./;${PKG}-${VER}/;" \
		-zcvf rpmbuild/SOURCES/${PKG}-${VER}.tar.gz ./
	rpmbuild --define "_topdir $(shell pwd)/rpmbuild/" --undefine "dist" \
		-bs ${PKG}.spec

rpm: srpm
	rpmbuild --define "_topdir $(shell pwd)/rpmbuild/" \
		--rebuild rpmbuild/SRPMS/${PKG}-${VER}-*.src.rpm

clean:
	rm -rf rpmbuild
