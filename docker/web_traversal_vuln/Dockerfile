FROM php:8.2-apache

WORKDIR /var/www/html

COPY public/ /var/www/html/
COPY config/ /opt/vulnlab/config/

RUN mkdir -p /opt/vulnlab/config /opt/vulnlab/data \
    && cp /opt/vulnlab/config/internal-export.txt /opt/vulnlab/data/internal-export.txt
