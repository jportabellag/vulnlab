#!/bin/sh
set -eu

python3 /opt/vulnlab/internal_service.py &

exec "$@"
