FROM python:3.5-slim-stretch

# Install build essentials
RUN set -x && \
    pip3 install --upgrade pip setuptools && \
    find / -name '*.py[co]' -delete

# Add and install project requirements file
COPY requirements.txt  /tmp/web-requirements.txt
RUN set -x && \
    pip install --no-cache-dir -r /tmp/web-requirements.txt && \
    find / -name '*.py[co]' -delete

# Set enviromental  variable for my predictionsapp
ENV APP_DIR=/service/project \
    PROJECT_DIR=/service \
    HTTP_SOCKET=0.0.0.0 \
    DEEVIO_USER=deevio \
    DEEVIO_GROUP=deevio

# Create non root user and groups.
RUN set -x && \
    groupadd --system --gid 1000 $DEEVIO_GROUP && \
    useradd --system --gid $DEEVIO_GROUP --uid 1000 -m $DEEVIO_USER

# Add source code
COPY . /service

# Link ctl.sh to /usr/local/bin
RUN ln -s $PROJECT_DIR/ctl.sh /usr/local/bin/app-ctl

# Switch working directory to source code.
WORKDIR $APP_DIR

# Pass version name and date during build, and persist in the img as env vars.
ARG BUILD_VERSION
ARG BUILD_SHA
ARG BUILD_DATE
ENV BUILD_VERSION=$BRAINANCE_BUILD_VERSION \
    BUILD_SHA=$BRAINANCE_BUILD_SHA \
    BUILD_DATE=$BRAINANCE_BUILD_DATE
