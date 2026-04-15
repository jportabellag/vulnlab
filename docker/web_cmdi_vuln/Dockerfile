FROM php:8.2-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY public/ /var/www/html/

EXPOSE 80

CMD ["apache2-foreground"]
