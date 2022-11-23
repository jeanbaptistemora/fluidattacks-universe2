FROM leafney/docker-alpine-mysql

RUN apk update && apk upgrade && apk add openssh
RUN ssh-keygen -A && \
    adduser -D -s /bin/sh nonpriv && \
    echo "root:Puef8poh2tei9AeB" | chpasswd && \
    echo "nonpriv:ahgh7xee9eewaeGh" | chpasswd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

ENTRYPOINT []
CMD /usr/sbin/sshd -D
