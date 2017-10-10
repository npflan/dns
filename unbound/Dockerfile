FROM alpine:3.6

ADD https://www.internic.net/domain/named.cache /etc/unbound/root.hints
RUN apk add --no-cache unbound drill \
    && unbound-anchor -v -a "/etc/unbound/root.key"; exit 0 \
    && chmod +r /etc/unbound/root.*

ENTRYPOINT ["/usr/sbin/unbound", "-d"]
EXPOSE 53/udp 53/tcp