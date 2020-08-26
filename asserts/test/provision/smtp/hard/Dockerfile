FROM registry.gitlab.com/fluidattacks/asserts/mocks/smtp:weak

ENV FLAVOR hard

EXPOSE 25/tcp

COPY etc_postfix_main.cf-hard /etc/postfix/main.cf

ENTRYPOINT ["/usr/libexec/postfix/master", "-c", "/etc/postfix", "-d"]
