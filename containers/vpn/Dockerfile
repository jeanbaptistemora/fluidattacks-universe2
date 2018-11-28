FROM registry.gitlab.com/fluidsignal/serves:base

ARG vault_pass

ADD . /root/

RUN echo "$vault_pass" > .vault.txt \
    && ansible-playbook main.yml --vault-password-file .vault.txt \
    && rm -rf \
        /root/* \
        /var/lib/apt/lists/*

EXPOSE 443

CMD run
