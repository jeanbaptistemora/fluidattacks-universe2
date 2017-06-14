# Base image
FROM python:2-onbuild

# Maintainer email
MAINTAINER FLUID Engineering Team <engineering@fluid.la>

# COPY startup script into known file location in container
COPY deploy/files/start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!
