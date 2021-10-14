import requests
import re
from ipaddress import ip_address
import ipaddress


class netbox:
    def __init__(self, token):
        self.token = token
        self.auth_header = {"Authorization": "Token {}".format(self.token)}

    def get_ip_addresses_reverse(self, sub_domain: str, ip_network: str, lenght: int):
        zone = ''
        try:
            data = requests.get(
                f"https://netbox.minserver.dk/api/ipam/ip-addresses/?limit=500&dns_name__ic={sub_domain}",
                headers=self.auth_header).json()
        except Exception as e:
            print(f"Request failed {e}")
        for line in data["results"]:
            if line['dns_name'] != "":

                address = re.search("([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})", line["address"]).group(0)
                if ipaddress.ip_address(address) in ipaddress.ip_network(ip_network):
                    reverse_address = str(ip_address(address).reverse_pointer).split(".")
                    reverse_address = ".".join(reverse_address[:lenght])
                    zone += "    {} IN PTR {}\n".format(reverse_address, line['dns_name'])

        return zone

    def get_ip_addresses(self, sub_domain: str):
        zone = ''
        try:
            data = requests.get(
                f"https://netbox.minserver.dk/api/ipam/ip-addresses/?limit=500&dns_name__ic={sub_domain}",
                headers=self.auth_header).json()
        except Exception as e:
            print(f"Request failed {e}")
        for line in data["results"]:
            address = re.search("([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})", line["address"]).group(0)
            zone += "    {} IN A {}\n".format(line['dns_name'].replace(f'.{sub_domain}.npf', ''), address)
        return zone