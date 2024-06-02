# Github Pages

> [INFO]
>
> This page is about maintaining RAIDOC.

> [DANGER]
>
> This page contains elevated quantities of salt

RAIDOC is hosted with github pages.
Github pages is a service for hosting static HTML sites.
RAIDOC is compiled to HTML and deployed to pages
using a thing called "github actions".
Actions is basically a hook that runs code whenever something
gets committed to `main` branch.
The actions configurations is inside of `.github/workflows/deploy.md`.

Where does the code run?
Inside of a "runner".
Github provides their own runners,
but I went with self-hosted.
For now,
the runner for RAIDOC
is emprisoned inside of a docker container on my laptop.
The dockerfile is as follows:

```Dockerfile
#FROM alpine:latest
#FROM ghcr.io/void-linux/void-glibc-busybox:46f5dc6
FROM ghcr.io/void-linux/void-glibc-full:46f5dc6
# glibc is needed for the runner
# gnu tar as opposed to busybox tar is needed for upload artifact action!?!

ARG GH_TOKEN
RUN test "$GH_TOKEN" || { echo "need github token"; exit 1; }

WORKDIR actions-runner 

RUN \
	`# apk update `&& \
	`#apk add` \
	`#	curl` \
	`#	perl-utils` `# for shasum` \
	`#	bash` \
	`#	dotnet6-sdk` `# screw you microsoft!! ` && \ 
	xbps-install -Syu \
		curl \
		bash \
		perl `# for shasum`\
		shadow `# for useradd and groupadd` \
		icu icu-libs `# for github runner` \
		`# the rest are for raidoc` \
		graphviz \
		python3

RUN \
	curl -o microsoft-sucks.tar.gz -L 'https://download.visualstudio.microsoft.com/download/pr/886b4a4c-30af-454b-8bec-81c72b7b4e1f/d1a0c8de9abb36d8535363ede4a15de6/dotnet-sdk-3.0.100-linux-x64.tar.gz' && \
	mkdir /microsoft-sucks && \
	tar xzf microsoft-sucks.tar.gz -C /microsoft-sucks

RUN \
	curl -o actions-runner-linux-x64-2.316.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz && \
	echo "d62de2400eeeacd195db91e2ff011bfb646cd5d85545e81d8f78c436183e09a8  actions-runner-linux-x64-2.316.1.tar.gz" | shasum -a 256 -c && \
	tar xzf ./actions-runner-linux-x64-2.316.1.tar.gz

RUN \
	`#addgroup -S runner` && \
	`#adduser -S runner -G runner` && \
	groupadd runner && \
	useradd runner -g runner && \
	chown -R runner:runner .

USER runner
ENV DOTNET_ROOT=/microsoft-sucks

RUN \
	./config.sh \
		--url https://github.com/maybeetree/raidoc \
		--token "$GH_TOKEN" \
		--agent "orth-docker-void"

ENTRYPOINT ["./run.sh"]
```

If it is not obvious from the dockerfile,
I am upset with github somehow needing full glibc, gnu coreutils,
and dotnet to make a program whose only purpose is to download code,
run it, and upload artifacts.
This wouldn't've been an issue with gitlab,
since their runner software is made by intelligent people,
not microsoft employees.

