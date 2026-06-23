#!/bin/sh

eecho() { echo "$@" >&2 ; }
die() { eecho "$@"; exit 1; }
cd_ass() { cd "$1" || die "Failed to cd into ${2:-$1}" ; }
ass() { "$@" || die "Failed to run command: $@" ; }

ass pip install -r ./raimad.requirement.txt
raimad_path="$(
	pip show raimad | tac | grep -e '^Location: .*$' | tail -c +11
	)" || die "failed to get raimad path"
[ -n "$raimad_path" ] || die "raimad path empty"
ass ln -sf "$raimad_path" ./raimad-symlink

