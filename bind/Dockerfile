FROM alpine:3.6

RUN apk add --no-cache kea python3 ca-certificates

EXPOSE 67/udp 67/tcp 647/tcp

ENTRYPOINT ["/usr/sbin/named", "-g", "-c", "/etc/named.conf"]