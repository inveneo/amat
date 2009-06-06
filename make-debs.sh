#!/bin/sh

# make-debs.sh - create .deb files

# it is a bit tricky because of the symlink to other svn directory for the
# common.py stuff

VERSION=1.0
EMAIL=support@inveneo.org

export DEBEMAIL=${EMAIL}
export DEBFULLNAME="Inveneo Inc"

# start with a clean slate
WORKDIR=debwork
rm -rf ${WORKDIR}

# populate work area with just desired source files (no links)
PACKAGE=amatd
PKGDIR=${PACKAGE}-${VERSION}
mkdir -p ${WORKDIR}/${PKGDIR}
cp client/* ${WORKDIR}/${PKGDIR}

# enter work area, make tarball, return
cd ${WORKDIR}
tar czf ${PACKAGE}_${VERSION}.orig.tar.gz ${PKGDIR}
cd ..

# copy debuild files, descend, run debuild, return
mkdir -p ${WORKDIR}/${PKGDIR}/debian
cp client/debian/* ${WORKDIR}/${PKGDIR}/debian
cd ${WORKDIR}/${PKGDIR}
debuild
cd ../..

echo "================================================================="
echo "Your .deb file(s) should now be found in ./debwork ... good luck!"
echo "Test it with ... $ sudo dpkg --install ./debwork/*deb"
