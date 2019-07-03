#!/usr/bin/env bash

# Exit with error if any command returns non zero code.
set -e
# Exit with error if any undefined variable is referenced.
set -u

# Get current directory
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PULL=

USAGE="Usage: $0 [options] <version>

Options:
    -h          Display this help message.
    -p          Pull base image before building.

Positional arguments:
    <version>   Version of software (probably branch/tag name or commit sha).
                This is used as the image tag.
"

log() { echo "$@" >&2; }

while getopts "hp" opt; do
    case "$opt" in
        h)
            echo "$USAGE"
            exit
            ;;
        p)
            PULL=1
            ;;
        \?)
            log "$USAGE"
            log
            log "ERROR: Invalid option: -$OPTARG"
            exit 1
    esac
done
shift $((OPTIND-1))

if [ "$#" -eq 0 ]; then
    log "$USAGE"
    log
    log "ERROR: No version/tag specified."
    exit 1
fi
if [ "$#" -gt 1 ]; then
    log "$USAGE"
    log
    log "ERROR: Multiple version/tag specified."
    exit 1
fi
TAG=$1

if [ -z "$PULL" ]; then
    BUILD_ARGS=""
else
    BUILD_ARGS="--pull"
fi

WEB_IMG="deeviochal:$TAG"
DEV_IMG="deeviochal/dev:$TAG"
NGINX_IMG="nginx:$TAG"

log "Will build images"
log "web:               $WEB_IMG"
# log "dev:               $DEV_IMG"
# log "nginx:             $NGINX_IMG"
log
log

log "Building app image"
log
set -x
docker build -t $WEB_IMG \
    --build-arg=BUILD_VERSION=$TAG \
    --build-arg=BUILD_SHA=${CI_COMMIT_SHA:-$(git rev-parse HEAD)} \
    --build-arg=BUILD_DATE="$(date -u '+%Y-%M-%d %H:%m:%S')" \
    -f $DIR/Dockerfile $DIR
set +x
log
log

# log "Building app dev image"
# log
# set -x
# sed -E "s|^FROM .+$|FROM $WEB_IMG|" $DIR/Dockerfile \
#     > $DIR/docker/dev/Dockerfile-dev
# docker build -t $DEV_IMG -f $DIR/docker/dev/Dockerfile.tmp $DIR/docker/dev
# set +x
# log
# log

# log "Building nginx image with static files"
# log
# set -x
# docker run --rm \
#     -v $DIR/docker/nginx/static:/tomotech-web/tomotech/web/static \
#     $WEB_IMG \
#     /tomotech-web/tomotech/web/manage.py collectstatic --noinput
# docker run --rm \
#     -v $DIR/docker/nginx/static/app:/dist \
#     $UI_IMG \
#     cp -a /tomotech-ui/dist/. /dist
# docker build $BUILD_ARGS -t $NGINX_IMG $DIR/docker/nginx
# docker run --rm -v $DIR/docker/nginx/:/mnt/nginx $WEB_IMG \
#     rm -rf /mnt/nginx/static
# set +x
# log
# log


log "Built images"
log
log "web:               $WEB_IMG"
# log "dev:               $DEV_IMG"
# log "nginx:             $NGINX_IMG"
