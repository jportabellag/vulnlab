FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends vsftpd \
    && rm -rf /var/lib/apt/lists/*

COPY vsftpd.conf /etc/vsftpd.conf
COPY start.sh /opt/vulnlab/start.sh

RUN chmod +x /opt/vulnlab/start.sh \
    && mkdir -p /srv/ftp/public /srv/ftp/backups /var/run/vsftpd/empty \
    && printf "Anonymous FTP server for training.\n" > /srv/ftp/public/readme.txt \
    && printf "legacy_user=webadmin\nlegacy_pass=Summer2024!\n" > /srv/ftp/backups/credentials.txt \
    && printf "backup placeholder\n" > /srv/ftp/backups/site-backup.zip

EXPOSE 21

CMD ["/opt/vulnlab/start.sh"]
