FROM alpine:3.6

RUN apk add --no-cache bind bind-tools \
    && mkdir -p /var/named \
    && mkdir -p /run/named

EXPOSE 5353/udp 5353/tcp

ENTRYPOINT ["/usr/sbin/named", "-g", "-c", "/etc/named.conf"]