FROM alpine:latest

RUN apk update && apk upgrade && apk add gcc openssh
RUN ssh-keygen -A && \
    adduser -D -s /bin/sh nonpriv && \
    echo "root:Puef8poh2tei9AeB" | chpasswd && \
    echo "nonpriv:ahgh7xee9eewaeGh" | chpasswd && \
    sed -i -e 's/^umask.*/umask 0022/g' /etc/profile && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "Ciphers aes128-cbc" >> /etc/ssh/sshd_config

CMD /usr/sbin/sshd -D
