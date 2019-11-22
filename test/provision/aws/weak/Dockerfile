FROM localstack/localstack

# localstack does not use full iam authentication but boto3 if required
ENV AWS_ACCESS_KEY_ID=foobar
ENV AWS_SECRET_ACCESS_KEY=foobar

ENV DOCKER_HOST=unix:///var/run/docker.sock
ENV LOCALSTACK_API_KEY='SOME-VALUE'

RUN pip3 install boto3

COPY . /scripts

