FROM golang:alpine

WORKDIR /go/src/app

RUN apk add --no-cache git
RUN go get github.com/kumina/unbound_exporter \
    && go install github.com/kumina/unbound_exporter

ENTRYPOINT ["unbound_exporter", "-unbound.host=localhost:8953"]