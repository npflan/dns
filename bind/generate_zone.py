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
dash IN CNAME v1-grafana.monitoring.svc.cluster.local.
prom IN CNAME prometheus.monitoring.svc.cluster.local.
kube IN CNAME kubernetes-dashboard.kube-system.svc.cluster.local.
alert IN CNAME alertmanager.monitoring.svc.cluster.local.
avatar IN A 10.0.0.1
ragnarok IN A 10.0.0.5
kubectl IN A 172.20.11.100
chimera IN A 172.20.11.101
archon IN A 172.20.22.101
scriptserver01 IN A 10.0.1.15
"""

zone = header.replace(
    '{{YMDS}}',
    '{:%Y%m%d}{:02d}'.format(
        datetime.date.today(),
        datetime.datetime.now().hour + 10 + datetime.datetime.now().minute//10
    )
)


participants = os.path.join(os.path.dirname(__file__), 'network_data_participants.csv')
others = os.path.join(os.path.dirname(__file__), 'network_data_other.csv')


distmap = defaultdict(lambda: [])
accessmap = {}
for f in pathlib.Path(pathlib.Path(__file__).parent, 'participants').glob('dist*.txt'):
    distname = f.stem[0] + f.stem[4:]
    with f.open() as d:
        for line in d:
            name = line.casefold()[:3]
            distmap[distname].append(name)
            accessmap[name] = distname

othernames = []
for f in pathlib.Path(pathlib.Path(__file__).parent, 'other').glob('*.txt'):
    with f.open() as d:
        for line in d:
            othernames.append(line.casefold().strip())

# print(accessmap)
# sys.exit(0)

def gen(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['name', 'ip', 'gateway'],
                                delimiter=',', quotechar='"')
        for row in reader:
            yield '{} IN A {}'.format(row['name'], row['ip'])
            if row['name'] in accessmap:
                yield '{}.{} IN CNAME {}.access.npf.'.format(row['name'], accessmap[row['name']], row['name'])

def telemetry():
    for switch, dist in accessmap.items():
        yield 'telemetry IN SRV 0 0 9167 {}.{}.access.npf.'.format(switch, dist)
    for switch in othernames:
        yield 'telemetry IN SRV 0 0 9167 {}.'.format(switch)

zone = zone + '\n$ORIGIN access.npf.\n'
zone = zone + '\n'.join(gen(participants)) + '\n'
zone = zone + '\n'.join(gen(others)) + '\n'
zone = zone + '\n'.join(telemetry()) + '\n'
zone = zone + '\n\n'
zone = zone + open(os.path.join(os.path.dirname(__file__), 'dist')).read()
print(zone)