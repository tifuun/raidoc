#!/bin/sh

set -e

# Make source folder of bind mounts, because
# podman will error out if they dont exist
mkdir -p build
mkdir -p venv

podman run \
	`# connect terminal to container process so you can cancel it ` \
	`# with ctrl-c. This will also enable colors in pip: ` \
	-ti \
	`# Remove container after run` \
	--rm \
	`# We won't need to write into out container directories, ` \
	`# so make it read-only ` \
	--read-only \
	`# Mount current dir into container read-only: ` \
	-v .:/pwd:ro \
	`# Make venv and build directories read-write tho: ` \
	-v ./venv:/pwd/venv:rw \
	-v ./build:/pwd/build:rw \
	-v ../raimad/src/raimad:/pwd/venv/lib/python3.12/site-packages/raimad:ro \
	`# Pip needs to dump some stuff into the src directory, ` \
	`# make it a tmpfs because we don't need it: ` \
	--tmpfs /pwd/src/raidoc.egg-info \
	`# root/.cache needs to be writeable for build process` \
	--tmpfs /root/.cache \
	raidoc-builder \
	"$@"

set +e


