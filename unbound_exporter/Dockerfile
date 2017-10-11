FROM golang:alpine

WORKDIR /go/src/app

ADD trusted-key.key /etc/unbound/
ADD unbound_control.key /etc/unbound/
ADD unbound_control.pem /etc/unbound/
ADD unbound_server.key /etc/unbound/
ADD unbound_server.pem /etc/unbound/

RUN apk update
RUN apk add git
RUN go get github.com/kumina/unbound_exporter
RUN go install github.com/kumina/unbound_exporter

ENTRYPOINT ["unbound_exporter", "-unbound.host=localhost:8953"]