#!/bin/sh

set -e
git config --global --add safe.directory "$(pwd)"
tagname=$(git describe --tags --abbrev=0)
mv "build" "raidoc-${tagname}-web"
tar cf - "raidoc-${tagname}-web" | \
	zstd --compress --ultra -20 --threads=0 - -o "raidoc-${tagname}-web.tar.zst"
mv "raidoc-${tagname}-web" "build"
ls -lah
set +e

