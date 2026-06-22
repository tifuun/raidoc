FROM ghcr.io/void-linux/void-glibc-full

# This is the default path but specify anyway to make sure
# cache mounts are in the right place
ENV GOCACHE=/root/.cache/go-build

# Cache mounts:
# 
# Golang modules:                    /go/pkg/mod
# Go build cache:                    /root/.cache/go-build
#                                    
# Python pip modules:                /root/.cache/pip
#                                    
# XBPS (System package manager)      /var/cache/xbps

RUN \
	\
	--mount=type=cache,target=/go/pkg/mod \
	--mount=type=cache,target=/root/.cache/go-build \
	\
	--mount=type=cache,target=/root/.cache/pip \
	\
	--mount=type=cache,target=/var/cache/xbps \
	\
	\
	`                     ` \
	`                     ` \
	`#################### ` \
	`# Prepare container  ` \
	`#################### ` \
	`                     ` \
	`                     ` \
	`# don't skip man pages ` \
	rm -rf /etc/xbps.d/noextract* && \
	`# xbps self-update must be separate command ` \
	xbps-install -Syu xbps && \
	`                     ` \
	`                     ` \
	`#################### ` \
	`# System pkgs        ` \
	`#################### ` \
	`                     ` \
	`                     ` \
	xbps-install -Syu \
		go `# Go Programming Language: called "golang" on other distros ` \
		graphviz \
		python3 \
		zstd \
		git \
		&& \
	`               ` \
	`               ` \
	`############## ` \
	`# Setup python ` \
	`############## ` \
	`               ` \
	`               ` \
	python3 -m venv /venv && \
	mkdir -p /etc/profile.d && \
	echo '. /venv/bin/activate' > /etc/profile.d/90-venv.sh && \
	chmod +x /etc/profile.d/90-venv.sh && \
	. /venv/bin/activate && \
	`               ` \
	`               ` \
	`############## ` \
	`# Setup golang ` \
	`############## ` \
	`               ` \
	`               ` \
	go install github.com/blampe/goat/cmd/goat@v0.2.0 && \
	ln -sf ~/go/bin/goat /bin/goat && \
	:


COPY . /app

WORKDIR /app

RUN /venv/bin/pip install -e .


#WORKDIR /pwd
#ENV PATH="$PATH:/root/go/bin"
#CMD ["/pwd/podman/build-raidoc-in-container.sh"]

