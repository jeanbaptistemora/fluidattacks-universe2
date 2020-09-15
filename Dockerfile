FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

COPY ./asserts /code/asserts
COPY ./bin /code/bin
COPY ./build /code/build
COPY ./forces /code/forces
COPY ./melts /code/melts
COPY ./skims /code/skims
COPY ./reviews /code/reviews
COPY ./.envrc.public /code/.envrc.public
COPY ./build.sh /code/build.sh
COPY ./default.nix /code/default.nix
COPY ./install.sh /code/install.sh

WORKDIR /code

RUN ./install.sh
