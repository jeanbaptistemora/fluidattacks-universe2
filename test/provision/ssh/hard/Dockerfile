# Official image for alpine linux
# This image comes with openssh compiled without
# SSH1 support
FROM alpine:3.11

# Installs SSH server
# Generates host keys
RUN apk update \
    && apk upgrade \
    && apk add --no-cache openssh \
    && ssh-keygen -A \
    && rm -rf /var/cache/apk/* \
    && echo "root:root123" | chpasswd \
    && adduser -D -s /bin/ash faustino \
    && echo "faustino:faustino123" | chpasswd

# Exposes container SSH port
EXPOSE 22

# Copy mock config
COPY entry.sh /
COPY sshd_config /etc/ssh/
COPY banner /etc/

# Startup command
ENTRYPOINT ["/entry.sh"]