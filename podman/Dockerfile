#FROM ghcr.io/void-linux/void-glibc-full
#
#RUN xbps-install -Syu \
#	python3 \
#	graphviz
#
#WORKDIR /pwd

FROM alpine:latest

RUN apk add --no-cache \
		graphviz \
		python3 \
		zstd \
		gcc \
		g++ \
		python3-dev \
		musl-dev \
		linux-headers \
		go \
		git \
		entr \
		&& \
	go install github.com/blampe/goat/cmd/goat@latest && \
	:

WORKDIR /pwd
ENV PATH="$PATH:/root/go/bin"
CMD ["/pwd/podman/build-raidoc-in-container.sh"]

