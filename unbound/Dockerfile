FROM alpine:3.6

ADD https://www.internic.net/domain/named.cache /etc/unbound/root.hints

ADD trusted-key.key /etc/unbound/trusted-key.key
ADD unbound_control.key /etc/unbound/unbound_control.key
ADD unbound_control.pem /etc/unbound/unbound_control.pem
ADD unbound_server.key /etc/unbound/unbound_server.key
ADD unbound_server.pem /etc/unbound/unbound_server.pem

RUN apk add --no-cache unbound drill \
    && unbound-anchor -v -a "/etc/unbound/root.key"; exit 0 \
    && chmod +r /etc/unbound/root.*

ENTRYPOINT ["/usr/sbin/unbound", "-d"]
EXPOSE 53/udp 53/tcp