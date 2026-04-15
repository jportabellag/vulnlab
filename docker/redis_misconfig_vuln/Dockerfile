FROM redis:7-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf
COPY entrypoint.sh /opt/vulnlab/entrypoint.sh

RUN chmod +x /opt/vulnlab/entrypoint.sh

EXPOSE 6379

CMD ["/opt/vulnlab/entrypoint.sh"]
