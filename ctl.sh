#!/bin/sh

set -e

_warmdb() {
    set +x
    su -m -c "python3 cli_utils/classification_publisher.py warmdb" - $DEEVIO_USER
    return
}

_pubmqtt() {
    set +x
    su -m -c "python3 cli_utils/classification_publisher.py pubmqtt" - $DEEVIO_USER &
    return
}

_preinit() {
    set +x
    # python3 -m pytest
    echo "Lint with flake8" >&2
    su -m -c "flake8 --count" - $DEEVIO_USER
    echo "Pytest and Coverage report" >&2
    su -m -c "coverage run -m pytest" - $DEEVIO_USER
    su -m -c "coverage report --include=\"predictionsapp/*\"" - $DEEVIO_USER
    return
}

_postinit() {
    return
}

prodinit() {
    set -x
    _preinit
    su -m -c "flask run --host $HTTP_SOCKET" - $DEEVIO_USER
    _postinit
}

devinit() {
    set -x
    _preinit
    _warmdb
    _pubmqtt
    su -m -c "flask run --host $HTTP_SOCKET" - $DEEVIO_USER
    _postinit
}


SELF="$0"

USAGE="$SELF <command>

Main entrypoint for operations and processes of tomotech inside docker
container.

Commands:
    init <profile>  Set up environment according to <profile>. Possible values
                    for profile are:
                        dev:
                            - ...
                        prod:
                            - ...
                files, create admin user etc.
    test        Run the automated test for the application and get coverage.
    lint        Run flake8 linter on the application code.
    help        Display this help message.

"

CMD="$1"
if [ -n "$CMD" ]; then
    shift
fi

case "$CMD" in
    init)
        if [ "$1" = "dev" ]; then
            devinit
        elif [ "$1" = "prod" ]; then
            prodinit
        elif [ -z "$1" ]; then
            echo "No init profile specified." >&2
            exit 1
        else
            echo "Invalid init profile specified." >&2
            exit 1
        fi
        ;;
    lint)
        run_linter $@
        ;;
    test)
        run_tester $@
        ;;
    help|--help|-h)
        echo "$USAGE"
        ;;
    *)
        echo "$USAGE" >&2
        echo "Wrong invocation." >&2
        exit 1
        ;;
esac
