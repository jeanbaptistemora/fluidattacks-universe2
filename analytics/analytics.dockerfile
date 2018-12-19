# ====[ prepare an static enviroment that can be cached ]=========
FROM alpine:edge AS base_enviroment

RUN apk update                                                   \
    &&  apk --no-cache --update --virtual build-dep add          \
            linux-headers                                        \
            libc-dev                                             \
            gcc                                                  \
            python3-dev                                          \
    &&  python3 -m ensurepip                                     \
    &&  python3 -m pip install --upgrade                         \
            pip                                                  \
            wheel                                                \
            setuptools                                           \
    &&  python3 -m pip install                                   \
            target-stitch                                        \
            boto3                                                \
    &&  rm -fr /usr/lib/python*/ensurepip                        \
    &&  rm -fr /var/cache/apk/*                                  \
    &&  rm -fr /root/.cache                                      \
    &&  rm -fr /tmp/*

# ====[ add a non-static enviroment in top of it ]================
FROM base_enviroment AS deployed_enviroment

COPY /analytics/conf   /conf
COPY /analytics/singer /singer

RUN mkdir /logs                                                  \
    &&  python3 -m pip install                                   \
            /singer/tap_currencyconverterapi                     \
            /singer/tap_awsdynamodb                              \
            /singer/tap_formstack
