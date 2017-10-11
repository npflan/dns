# NPF DNS on Kubernetes

This repos hold our unbound recursive, validating secure DNS resolver, and bind for local zones (.npf & .cluster.local)

### Quickstart

``` shell
kubectl create namespace dns
kubectl apply -f unbound.conf.yml
kubectl apply -f bind.conf.yml
kubectl apply -f unbound.yml
kubectl apply -f bind.yml
```

