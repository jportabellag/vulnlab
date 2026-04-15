#!/bin/sh
set -eu

redis-server /usr/local/etc/redis/redis.conf &
REDIS_PID=$!

sleep 1

redis-cli SET public:welcome "Cache node ready for staging clients"
redis-cli SET cache:theme "teal"
redis-cli SET queue:workers "4"
redis-cli HSET ops:sync service redis-sync username sync-user password sync-redis-2024
redis-cli HSET ops:snapshot location /data/dump.rdb owner cache-admin schedule nightly
redis-cli SET notes:legacy "Do not expose this node outside the private network"
redis-cli SAVE >/dev/null

wait "$REDIS_PID"
