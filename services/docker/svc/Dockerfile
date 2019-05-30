FROM  centos:centos7

RUN mkdir -p /code /scripts /etc/named/zones
WORKDIR /code
RUN yum update --assumeyes --skip-broken && \
    yum install --assumeyes iproute vim bind bind-utils

COPY docker/svc/entrypoint.sh /scripts/
COPY bind/etc /etc
