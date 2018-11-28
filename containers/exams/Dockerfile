FROM registry.gitlab.com/fluidsignal/serves:base

ARG vault_pass

ADD . /root/

RUN echo "$vault_pass" > .vault.txt \
    && ansible-playbook main.yml --vault-password-file .vault.txt \
    && rm -rf \
        /root/* \
        /var/lib/apt/lists/*

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND && php /var/www/html/admin/cli/purge_caches.php
