FROM alpine:latest

ENV FLAVOR weak

EXPOSE 139/tcp 445/tcp 135/udp 139/udp

RUN apk update && apk upgrade && apk add samba
RUN adduser -D -s /bin/sh nonpriv && \
    echo "root:Puef8poh2tei9AeB" | chpasswd && \
    echo "nonpriv:ahgh7xee9eewaeGh" | chpasswd && \
    (echo "Puef8poh2tei9AeB"; echo "Puef8poh2tei9AeB") | smbpasswd -a root && \
    (echo "ahgh7xee9eewaeGh"; echo "ahgh7xee9eewaeGh") | smbpasswd -a nonpriv && \
    mkdir -p /samba/public && \
    mkdir -p /samba/private && \
    touch /samba/public/public_file.txt && \
    touch /samba/private/private_file.txt

COPY etc_samba_smb.conf-weak /etc/samba/smb.conf

CMD /usr/sbin/smbd -FS --no-process-group
