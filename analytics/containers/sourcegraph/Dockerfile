FROM sourcegraph/server:3.1.1

# sourcegraph_overrides.zip is a zip file read from:
#   https://s3.amazonaws.com/fluidanalytics/sourcegraph_overrides.zip
# it contains a hard-coded admin account
#   (otherwise the first user to login becomes admin on server restart)
# it contains discovered critical security patches (server configurations)
#   (like only allowing users to register through admin invitation)

COPY sourcegraph_overrides.zip /

RUN cd / \
    && unzip /sourcegraph_overrides.zip \
    && chown --recursive postgres:postgres /var/opt/sourcegraph/postgresql \
    && chown postgres:root /var/opt/sourcegraph/postgresql \
    && chmod -R 777 /etc/sourcegraph \
    && chmod -R 777 /var/opt/sourcegraph \
    && chmod -R 0750 /var/opt/sourcegraph/postgresql
