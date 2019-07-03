FROM python:3.5-slim-stretch

# Install build essentials
RUN set -x && \
    pip3 install --upgrade pip setuptools && \
    find / -name '*.py[co]' -delete

# Add requirements file
ADD requirements.txt ctl.sh .flake8 /opt/

# Install project requirements
RUN pip install --no-cache-dir -r /opt/requirements.txt

# Link ctl.sh to /usr/local/bin
RUN ln -s /opt/ctl.sh /usr/local/bin/app-ctl

# Add source code
COPY project/ /service/project

# Switch working directory to source code.
WORKDIR /service/project

# Set enviromental  variable for my predictionsapp
ENV PROJECT_DIR=/service/project \
    HTTP_SOCKET=0.0.0.0

# Pass version name and date during build, and persist in the img as env vars.
ARG BUILD_VERSION
ARG BUILD_SHA
ARG BUILD_DATE
ENV BUILD_VERSION=$BRAINANCE_BUILD_VERSION \
    BUILD_SHA=$BRAINANCE_BUILD_SHA \
    BUILD_DATE=$BRAINANCE_BUILD_DATE
