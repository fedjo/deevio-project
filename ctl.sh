#!/bin/sh

set -e

_preinit() {
    set +x
    # python3 -m pytest
    echo "Lint with flake8" >&2
    flake8 --count
    echo "Pytest and Coverage report" >&2
    coverage run -m pytest
    coverage report --include="predictionsapp/*"
    python3 cli_utils/classification_publisher.py warmdb
    python3 cli_utils/classification_publisher.py pubmqtt &
    return
}

_postinit() {
    return
}

prodinit() {
    set -x
    _preinit
    _postinit
}

devinit() {
    set -x
    _preinit
    flask run --host $HTTP_SOCKET
    _postinit
}

run_tester() {
    set -x
    flask test
    $@
}

run_linter() {
    set -x
    flask lint
    $@
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
