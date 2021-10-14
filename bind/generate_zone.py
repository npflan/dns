import datetime
import csv
import os
import sys
import pathlib
from collections import defaultdict
from get_vlans import netbox

nb = netbox("TOKEN")
nb.get_ip_addresses("dist")

header = """
apiVersion: v1
metadata:
    name: bind
    namespace: dns
kind: ConfigMap
data:
  named.conf: |
    options {
        directory "/var/named";
        pid-file "/run/named/named.pid";
        listen-on-v6 { none; };
        listen-on port 5353 { any; };
        allow-recursion { none; };
        allow-transfer { none; };
        allow-update { none; };
        version none;
        hostname none;
        server-id none;
    };

    zone "npf" IN {
        type master;
        file "/bind/config/npf.zone";
        allow-update { none; };
    };

    zone "10.in-addr.arpa" IN {
        type master;
        file "/bind/config/10.in-addr.arpa.zone";
    };
    zone "168.192.in-addr.arpa" IN {
        type master;
        file "/bind/config/168.192.in-addr.arpa.zone";
    };
    zone "20.172.in-addr.arpa" IN {
        type master;
        file "/bind/config/20.172.in-addr.arpa.zone";
    };

  npf.zone: |
    $ORIGIN npf.
    $TTL 600

    @	IN	SOA	ns1.npf.	hostmaster.npf. (
        {{YMDS}} ; Serial
        300 ; Refresh
        150 ; Retry
        600 ; Expire
        600) ; Minimum

        IN	NS	ns1.npf.

    ns1			IN  A   10.96.5.3
    prom-server IN  A   10.101.128.200

    alert IN CNAME prometheus-alertmanager.prometheus.svc.cluster.local.
    argo IN CNAME argocd-server.argocd.svc.cluster.local.
    dash IN CNAME grafana.grafana.svc.cluster.local.
    gaas IN CNAME gaas-portal.gaas.svc.cluster.local.
    gaas-api IN CNAME gaas-api-service.gaas.svc.cluster.local.
    heatmap IN CNAME sw-heatmap.sw-heatmap.svc.cluster.local.
    prom IN CNAME prometheus-server.prometheus.svc.cluster.local.
    rtmp IN CNAME rtmp.rtmp.svc.cluster.local.
    shinobi IN CNAME shinobi.shinobi.svc.cluster.local.
    shutdown IN CNAME shutdown-svc.cisco.svc.cluster.local.

    avatar IN A 10.0.0.1
    leviathan IN A 10.0.0.5
    ragnarok IN A 10.0.0.9
    erebus IN A 10.0.0.13
    kubectl IN A 172.20.11.102
    chimera IN A 172.20.11.104
    archon IN A 172.20.22.104
"""

reverse_header_10 = """
    $ORIGIN 10.in-addr.arpa.
    $TTL 600

    @	IN	SOA	ns1.npf.	hostmaster.npf. (
        {{YMDS}} ; Serial
        300 ; Refresh
        150 ; Retry
        600 ; Expire
        600) ; Minimum

        IN	NS	ns1.npf.

"""

reverse_header_168_192 = """
    $ORIGIN 168.192.in-addr.arpa.
    $TTL 600

    @	IN	SOA	ns1.npf.	hostmaster.npf. (
        {{YMDS}} ; Serial
        300 ; Refresh
        150 ; Retry
        600 ; Expire
        600) ; Minimum

        IN	NS	ns1.npf.

"""

reverse_header_20_172 = """
    $ORIGIN 20.172.in-addr.arpa.
    $TTL 600

    @	IN	SOA	ns1.npf.	hostmaster.npf. (
        {{YMDS}} ; Serial
        300 ; Refresh
        150 ; Retry
        600 ; Expire
        600) ; Minimum

        IN	NS	ns1.npf.

"""

zone = header.replace(
    '{{YMDS}}',
    '{:%Y%m%d}{:02d}'.format(
        datetime.date.today(),
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute // 10
    )
)

reverse_zone_10 = reverse_header_10.replace(
    '{{YMDS}}',
    '{:%Y%m%d}{:02d}'.format(
        datetime.date.today(),
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute // 10
    )
)

reverse_zone_168_192 = reverse_header_168_192.replace(
    '{{YMDS}}',
    '{:%Y%m%d}{:02d}'.format(
        datetime.date.today(),
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute // 10
    )
)

reverse_zone_20_172 = reverse_header_20_172.replace(
    '{{YMDS}}',
    '{:%Y%m%d}{:02d}'.format(
        datetime.date.today(),
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute // 10
    )
)

dist_to_hostname_map = {'dist1': 'd1',
                        'dist2': 'd2',
                        'dist3': 'd3',
                        'dist4': 'd4',
                        'dist5': 'd5',
                        'dist6': 'd6',
                        'dist7': 'd7',
                        'dist8': 'd8',
                        'dist9': 'd9',
                        'dist10': 'd10',
                        'dist11': 'd11',
                        'dist12': 'd12',
                        'dist13': 'd13',
                        'dist14': 'd14',
                        'dist15': 'd15',
                        'dist16': 'd16'
                        }

network = os.path.join(os.path.dirname(__file__), 'network_data.csv')


def gen(filepath):
    with open(filepath, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            yield '{} IN A {}'.format(row['Hostname'], row['Mgmt IP'])
            if row['Distribution'] in dist_to_hostname_map:
                yield '{}.{} IN A {}'.format(row['Hostname'], dist_to_hostname_map[row['Distribution']],
                                                             row['Mgmt IP'])
                yield 'telemetry IN SRV 0 0 9167 {}.{}.access.npf.'.format(row['Hostname'],
                                                                           dist_to_hostname_map[row['Distribution']])
            else:
                yield '{}.{} IN A {}'.format(row['Hostname'], row['Distribution'], row['Mgmt IP'])
                yield 'telemetry IN SRV 0 0 9167 {}.{}.access.npf.'.format(row['Hostname'], row['Distribution'])


def gen_reverse(filepath):
    with open(filepath, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            ip_parts = row['Mgmt IP'].split('.')
            if row['Distribution'] in dist_to_hostname_map:
                yield '{}.{} IN PTR {}.{}.access.npf.'.format(ip_parts[3], ip_parts[2], row['Hostname'],
                                                              dist_to_hostname_map[row['Distribution']])
            else:
                yield '{}.{} IN PTR {}.{}.access.npf.'.format(ip_parts[3], ip_parts[2], row['Hostname'],
                                                              row['Distribution'])


# ORIGIN access.npf
zone = zone + '\n    $ORIGIN access.npf.\n    '
zone = zone + '\n    '.join(gen(network)) + '\n'
zone = zone + '\n\n'
# ORIGIN dist.npf
zone = zone + '{}\n'.format(open(os.path.join(os.path.dirname(__file__), 'dist')).read())
zone = zone + nb.get_ip_addresses("dist")
# ORIGIN link.npf
zone = zone + '\n    $ORIGIN link.npf.\n'
zone = zone + nb.get_ip_addresses("link")
# ORIGIN dc.npf
zone = zone + '\n    $ORIGIN dc.npf.\n'
zone = zone + nb.get_ip_addresses("dc")
# ORIGIN kube.npf
zone = zone + '\n    $ORIGIN kube.npf.\n'
zone = zone + nb.get_ip_addresses("kube")

## PTR
zone = zone + '\n  10.in-addr.arpa.zone: |'
zone = zone + reverse_zone_10
zone = zone + nb.get_ip_addresses_reverse('link', '10.0.0.0/8', 3)
zone = zone + nb.get_ip_addresses_reverse('dist', '10.0.0.0/8', 3)
zone = zone + nb.get_ip_addresses_reverse('kube', '10.0.0.0/8', 3)
#
zone = zone + '\n  168.192.in-addr.arpa.zone: |'
zone = zone + reverse_zone_168_192
zone = zone + nb.get_ip_addresses_reverse('link', '192.168.0.0/16', 2)
zone = zone + nb.get_ip_addresses_reverse('dist', '192.168.0.0/16', 2)
zone = zone + nb.get_ip_addresses_reverse('kube', '192.168.0.0/16', 2)
#
zone = zone + '\n  20.172.in-addr.arpa.zone: |'
zone = zone + reverse_zone_20_172
zone = zone + nb.get_ip_addresses_reverse('link', '172.16.0.0/12', 2)
zone = zone + nb.get_ip_addresses_reverse('dist', '172.16.0.0/12', 2)
zone = zone + nb.get_ip_addresses_reverse('kube', '172.16.0.0/12', 2)
print(zone)
