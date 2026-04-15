FROM php:8.2-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY public/ /var/www/html/
COPY scripts/internal_service.py /opt/vulnlab/internal_service.py
COPY scripts/entrypoint.sh /opt/vulnlab/entrypoint.sh

RUN chmod +x /opt/vulnlab/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/opt/vulnlab/entrypoint.sh"]
CMD ["apache2-foreground"]
