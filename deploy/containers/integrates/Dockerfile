# Imagen base del ultimo linux estable de Debian (jessie-slim)
FROM registry.gitlab.com/fluidsignal/integrates:deps

# Dudas sobre la imagen en cuestion
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

ARG ci_commit_ref_name
ARG aws_region
ARG aws_access_key_dynamodb
ARG aws_secret_key_dynamodb
ARG formstack_tokens

ENV DEBIAN_FRONTEND noninteractive      # instalación no interactiva
ENV CI_COMMIT_REF_NAME=$ci_commit_ref_name
ENV AWS_REGION=$aws_region
ENV AWS_ACCESS_KEY_DYNAMODB=$aws_access_key_dynamodb
ENV AWS_SECRET_KEY_DYNAMODB=$aws_secret_key_dynamodb
ENV FORMSTACK_TOKENS=$formstack_tokens
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Agrega el playbook
ADD common/main.yml /root/

# Agrega las variables
ADD common/vars* /root/vars

# Agrega el vault
ADD .vault.txt /root/

# Cambia al directorio root
WORKDIR /root/

# Ejecuta el ansible
RUN ansible-playbook main.yml --vault-password-file .vault.txt

# Make port 80 and 443 available to the world outside this container
EXPOSE 443

# Primer comando
CMD service cron start && /usr/sbin/apache2ctl -D FOREGROUND
