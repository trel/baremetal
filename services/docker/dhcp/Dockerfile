FROM  centos:centos7

RUN mkdir -p /code /scripts /etc/dhcp/conf.d
WORKDIR /code
RUN yum update --assumeyes --skip-broken && \
    yum install --assumeyes iproute vim dhcp

COPY docker/dhcp/entrypoint.sh /scripts/
COPY dhcp/etc /etc