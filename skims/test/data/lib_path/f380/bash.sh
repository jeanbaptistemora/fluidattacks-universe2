#!/bin/bash

#Vuln1 oneline
docker run -d -p 80:80 ubuntu:xenial -g 'daemon off;'

# Vuln2 multiple line
docker run -p 80:80 \
  ubuntu:xenial \
  -g 'daemon off;'

# NotVuln1 one line
docker run ubuntu@sha256:043a718774c572bd8a25adbeb1bfcd5c0256ae11cecf9f9c3f925d0e52beaf89 -g 'daemon off;'

# NotVuln2 one line
docker run -d -p 80:80 \
  ubuntu:21.01-lts@sha256:03042cf8100db386818cee4ff0f2972431a62ed78edbd09ac08accfabbefd818 \
  -g 'daemon off;'

# Control. Other lines with look alike commands
echo run ubuntu:xenial
echo run ubuntu@sha256:043a718774c572bd8a25adbeb1bfcd5c0256ae11cecf9f9c3f925d0e52beaf89
