#!/bin/sh
set -eu

mkdir -p /var/www/html/uploads
chmod 777 /var/www/html/uploads

exec "$@"
