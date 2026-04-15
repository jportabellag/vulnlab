#!/bin/sh
set -eu

exec /usr/sbin/vsftpd /etc/vsftpd.conf
