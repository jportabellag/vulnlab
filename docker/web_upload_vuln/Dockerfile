FROM php:8.2-apache

WORKDIR /var/www/html

COPY public/ /var/www/html/
COPY scripts/entrypoint.sh /opt/vulnlab/entrypoint.sh

RUN chmod +x /opt/vulnlab/entrypoint.sh \
    && mkdir -p /var/www/html/uploads

EXPOSE 80

ENTRYPOINT ["/opt/vulnlab/entrypoint.sh"]
CMD ["apache2-foreground"]
