FROM registry.gitlab.com/fluidattacks/asserts:runner

ENV FA_LICENSE_KEY=430e535360b03d3629c3b75fcf370b0862e0930201079beca9fde26d7744f6f1
ENV FA_USER_EMAIL=technology@fluid.la

ADD exploit.py /
ADD entrypoint.sh /
RUN chmod 0755 /entrypoint.sh

WORKDIR /code

ENTRYPOINT ["/entrypoint.sh"]
