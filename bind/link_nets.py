from ipaddress import ip_address
import requests
import sys
import re

HEADERS = {"Authorization": "Token "}

if len(sys.argv) < 2:
    print("Usage: python dns.py sub_domain ex: link or dist")
    sys.exit()
subdomain = sys.argv[1]

def get_addresses(sub_domain: str):
    try:
        data = requests.get(f"https://netbox.minserver.dk/api/ipam/ip-addresses/?limit=500&dns_name__ic={sub_domain}",headers=HEADERS).json()
    except Exception as e:
        print(f"Request failed {e}")

    print(f"A records for .{sub_domain}.npf:\r\n")
    for line in data["results"]:
        address = re.search("([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})", line["address"]).group(0)
        print(f"{line['dns_name'].replace(f'.{sub_domain}.npf','')} IN A {address}")
    print("----------------------------------------------")
    print(f"PTR records for .{sub_domain}.npf:\r\n")
    for line in data["results"]:
        if line['dns_name'] != "":
            address = re.search("([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})", line["address"]).group(0)
            print(f"{ip_address(address).reverse_pointer.replace('.in-addr.arpa','')} IN PTR {line['dns_name']}.")

if __name__ == "__main__":
    get_addresses(subdomain)
