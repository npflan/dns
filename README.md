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

### DNS Changes

Generate the zone with

``` shell
python3 bind/generate_zone.py
```

Log into a bind pod, and check the zone syntax

```Shell
named-checkzone -d npf /bind/config/npf.zone
```

