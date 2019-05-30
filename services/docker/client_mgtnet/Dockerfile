FROM  centos:centos7

RUN mkdir -p /code /scripts 
WORKDIR /code
RUN yum update --assumeyes --skip-broken && \
    yum install --assumeyes iproute vim bind-utils dhclient

COPY entrypoint.sh /scripts/