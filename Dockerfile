FROM nixos/nix:2.3.6

# Basic dependencies in the host needed to execute ./m
RUN apk add --no-cache \
      bash=5.0.17-r0 \
      git=2.26.2-r0

# The name of the branch, can be overriden on a per-job basis but is left here
# as a safe default value
ENV CI_COMMIT_REF_NAME=master

# Configure SSH, the host key verification is weakened on purpose because
# many jobs that run on this image connect to thousands of uknonwn providers
RUN mkdir -p ~/.ssh \
  &&  echo 'Host *' > ~/.ssh/config \
  &&  echo '  StrictHostKeyChecking no' >> ~/.ssh/config \
  &&  chmod 400 ~/.ssh/config

# Copy the source into the container, this serves as the context for ./build.sh
# and source code for the commands
COPY . /source
WORKDIR /source
