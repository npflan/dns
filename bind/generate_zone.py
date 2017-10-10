import datetime
import csv
import os

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

def gen(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['name', 'ip', 'gateway'],
                                delimiter=',', quotechar='"')
        for row in reader:
            yield '{} IN A {}'.format(row['name'], row['ip'])

zone = zone + '\n$ORIGIN access.npf.\n'
zone = zone + '\n'.join(gen(participants))
zone = zone + '\n'
zone = zone + '\n'.join(gen(others))
zone = zone + '\n\n'
zone = zone + open(os.path.join(os.path.dirname(__file__), 'dist')).read()
print(zone)