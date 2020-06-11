from nornir.core.deserializer.inventory import Inventory
import pandas as pd


class CustomInventory(Inventory):
    def __init__(self, **kwargs):

        hosts = self.get_file_content(kwargs["filename"])
        groups = {}
        defaults = {}

        super().__init__(hosts=hosts, groups=groups, defaults=defaults, **kwargs)

    def get_file_content(self, filename: str):
        # df : This host format can be used in netmiko directly.

        if ".csv" in filename.lower():
            df = pd.read_csv(filename)[['host', 'device_type', 'device_name']].to_dict(
                orient='records')
        else:
            df = pd.read_excel(filename)[['host', 'device_type', 'device_name']].to_dict(
                orient='records')
        hosts = {}
        for item in df:
            host = {
                item["device_name"]: {
                    'hostname': item["host"],
                    'platform': item["device_type"]
                }
            }
            hosts.update(host)
        return hosts