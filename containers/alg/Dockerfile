FROM registry.gitlab.com/fluidsignal/serves:base

ARG vault_pass

ADD . /root/

RUN echo "$vault_pass" > .vault.txt \
    && ansible-playbook main.yml --vault-password-file .vault.txt \
    && curl -L https://toolbelt.treasuredata.com/sh/install-debian-jessie-td-agent2.sh | sh \
        && rm /etc/td-agent/td-agent.conf \
        && mv vars/fluent.conf /etc/td-agent/td-agent.conf \
        && rm /etc/init.d/td-agent \
        && mv vars/td-agent /etc/init.d/td-agent && chmod 0755 /etc/init.d/td-agent  \
        && mv vars/out_rollbar.rb /etc/td-agent/plugin/ \
    && /usr/sbin/td-agent-gem install eventmachine em-http-request fluent-plugin-rewrite-tag-filter \
    && rm -rf \
        /root/* \
        /var/lib/apt/lists/*

EXPOSE 80
EXPOSE 443

CMD /etc/init.d/td-agent restart \
    && /usr/sbin/apache2ctl -D FOREGROUND
