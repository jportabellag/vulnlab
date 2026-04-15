#!/bin/sh
set -eu

mkdir -p /opt/vulnlab/data /var/www/html/backup

php /opt/vulnlab/init-db.php

cp /opt/vulnlab/data/app.db /var/www/html/backup/app.db.bak

exec "$@"
