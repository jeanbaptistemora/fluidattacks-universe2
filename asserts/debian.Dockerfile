FROM python:3.7.6-slim-buster AS light

RUN apt update \
    && apt upgrade -y \
    && apt-get install -u -y \
        unixodbc \
        unixodbc-dev \
        build-essential \
        libgssapi-krb5-2 \
        wget \
        libpq-dev \
        curl \
    && pip3 install --no-cache-dir cython==0.29.14

RUN wget \
        -c https://packages.microsoft.com/debian/10/prod/pool/main/m/msodbcsql17/msodbcsql17_17.4.2.1-1_amd64.deb \
        -O /tmp/msodbcsql17.deb \
    && ACCEPT_EULA=Y dpkg -i /tmp/msodbcsql17.deb \
    && rm /tmp/msodbcsql17.deb

RUN pip3 install --upgrade fluidasserts

FROM light as full

# Remember that geckodriver, firefox, and selenium must be compatible
RUN apt-get install -y \
        firefox-esr \
        udev \
        xvfb \
    && wget \
          -c https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz \
          -O /tmp/geckodriver.tar.gz \
        && tar \
          -C /usr/local/bin/ \
          -xzf /tmp/geckodriver.tar.gz \
    && rm -rf /tmp/geckodriver.tar.gz

