FROM registry.gitlab.com/fluidsignal/asserts:runner

ENV FLUIDASSERTS_LICENSE_KEY=430e535360b03d3629c3b75fcf370b0862e0930201079beca9fde26d7744f6f1
ENV FLUIDASSERTS_USER_EMAIL=technology@fluid.la

ADD exploit.py /

WORKDIR /code

CMD python /exploit.py
