FROM dejankovacevic/gitlab:0.1.0

RUN apt update \
  && apt upgrade -y \
  && apt install -y \
    gettext-base=0.19.7*

COPY run-wire-gitlab-bot-service.sh .

CMD ["bash", "-c", ". run-wire-gitlab-bot-service.sh && run_wire_gitlab_bot_service"]
