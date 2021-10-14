import datetime
import csv
import os
import sys
import pathlib
from collections import defaultdict

header = """
$ORIGIN npf.
$TTL 600

@	IN	SOA	ns1.npf.	hostmaster.npf. (
		{{YMDS}} ; Serial
		300 ; Refresh
		150 ; Retry
		600 ; Expire
		600) ; Minimum

    IN	NS	ns1.npf.

ns1				IN	A	10.96.5.3
prom-server     IN  A   10.101.128.200
dash IN CNAME grafana.grafana.svc.cluster.local.
prom IN CNAME prometheus.prometheus.svc.cluster.local.
alert IN CNAME alertmanager.prometheus.svc.cluster.local.
shinobi IN CNAME shinobi.shinobi.svc.cluster.local.
heatmap IN CNAME sw-heatmap.sw-heatmap.svc.cluster.local.
gaas IN CNAME gaas-portal.gaas.svc.cluster.local.

avatar IN A 10.0.0.1
leviathan IN A 10.0.0.5
ragnarok IN A 10.0.0.9
erebus IN A 10.0.0.13
kubectl IN A 172.20.11.102
chimera IN A 172.20.11.104
archon IN A 172.20.22.104
scriptserver01 IN A 10.0.1.15
"""

reverse_header = """
$ORIGIN 255.10.in-addr.arpa.
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
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute//10
    )
)

reverse_zone = reverse_header.replace(
    '{{YMDS}}',
    '{:%Y%m%d}{:02d}'.format(
        datetime.date.today(),
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute//10
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


participants = os.path.join(os.path.dirname(__file__), 'network_data_participants.csv')
others = os.path.join(os.path.dirname(__file__), 'network_data_other.csv')
network = os.path.join(os.path.dirname(__file__), 'network_data.csv')



def gen(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            yield '{} IN A {}'.format(row['Hostname'], row['Mgmt IP'])
            if row['Distribution'] in dist_to_hostname_map:
                yield '{}.{} IN CNAME {}.access.npf.'.format(row['Hostname'], dist_to_hostname_map[row['Distribution']], row['Hostname'])
                yield 'telemetry IN SRV 0 0 9167 {}.{}.access.npf.'.format(row['Hostname'], dist_to_hostname_map[row['Distribution']])
            else:
                yield '{}.{} IN CNAME {}.access.npf.'.format(row['Hostname'], row['Distribution'], row['Hostname'])
                yield 'telemetry IN SRV 0 0 9167 {}.{}.access.npf.'.format(row['Hostname'], row['Distribution'])

def gen_reverse(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            ip_parts = row['Mgmt IP'].split('.')
            if row['Distribution'] in dist_to_hostname_map:
                yield '{}.{} IN PTR {}.{}.access.npf.'.format(ip_parts[3], ip_parts[2], row['Hostname'], dist_to_hostname_map[row['Distribution']])
            else:
                yield '{}.{} IN PTR {}.{}.access.npf.'.format(ip_parts[3], ip_parts[2], row['Hostname'], row['Distribution'])


zone = zone + '\n$ORIGIN access.npf.\n'
#zone = zone + '\n'.join(gen(participants)) + '\n'
#zone = zone + '\n'.join(gen(others)) + '\n'
zone = zone + '\n'.join(gen(network)) + '\n'
zone = zone + '\n\n'
zone = zone + open(os.path.join(os.path.dirname(__file__), 'dist')).read()
print(zone)

#reverse_zone = reverse_zone + '\n'.join(gen_reverse(participants)) + '\n'
#reverse_zone = reverse_zone + '\n'.join(gen_reverse(others)) + '\n'
reverse_zone = reverse_zone + '\n'.join(gen_reverse(network)) + '\n'
reverse_zone = reverse_zone + open(os.path.join(os.path.dirname(__file__), 'dist_reverse')).read()
print(reverse_zone)
