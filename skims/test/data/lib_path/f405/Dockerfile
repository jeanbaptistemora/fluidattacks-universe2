FROM ubuntu:21.01-lts@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b676e23 AS ubuntu
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y nginx php-fpm supervisor && \
    useradd -ms /bin/bash newuser \
    rm -rf /var/lib/apt/lists/* && \
    sshpass -p !4u2tryhack ssh username@host.example.com \
    apt clean
    chmod 750 testfile
    chmod 754 testfile
