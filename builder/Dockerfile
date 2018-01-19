FROM docker:latest

WORKDIR /app

COPY . /app

RUN apk update && apk add curl && \
    curl -o terraform.zip https://releases.hashicorp.com/terraform/0.11.2/terraform_0.11.2_linux_amd64.zip && \
      unzip terraform.zip && rm terraform.zip && \
      cp terraform /bin/terraform && \
    curl -Lo tflint.zip https://github.com/wata727/tflint/releases/download/v0.5.4/tflint_linux_amd64.zip && \
      unzip tflint.zip && rm tflint.zip && \
      install tflint /bin && \
    apk --update add python python-dev py-pip && \
    pip install awscli

CMD ["bash"]
