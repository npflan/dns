FROM alpine:3.6

ADD https://www.internic.net/domain/named.cache /etc/unbound/root.hints
RUN apk add --no-cache unbound drill \
    && unbound-anchor -v -a "/etc/unbound/root.key"; exit 0 \
    && chmod +r /etc/unbound/root.*

ADD trusted-key.key /etc/unbound/
ADD unbound_control.key /etc/unbound/
ADD unbound_control.pem /etc/unbound/
ADD unbound_server.key /etc/unbound/
ADD unbound_server.pem /etc/unbound/

ENTRYPOINT ["/usr/sbin/unbound", "-d"]
EXPOSE 53/udp 53/tcp