FROM php:8.2-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsqlite3-dev \
    && docker-php-ext-install pdo_sqlite \
    && a2enmod rewrite \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY public/ /var/www/html/
COPY scripts/init-db.php /opt/vulnlab/init-db.php
COPY scripts/entrypoint.sh /opt/vulnlab/entrypoint.sh

RUN chmod +x /opt/vulnlab/entrypoint.sh \
    && mkdir -p /opt/vulnlab/data /var/www/html/backup

EXPOSE 80

ENTRYPOINT ["/opt/vulnlab/entrypoint.sh"]
CMD ["apache2-foreground"]
