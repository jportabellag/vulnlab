FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server sudo procps net-tools iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY setup.sh /opt/vulnlab/setup.sh
COPY sshd_config /etc/ssh/sshd_config
COPY start.sh /opt/vulnlab/start.sh

RUN chmod +x /opt/vulnlab/setup.sh /opt/vulnlab/start.sh \
    && /opt/vulnlab/setup.sh

EXPOSE 22

CMD ["/opt/vulnlab/start.sh"]
