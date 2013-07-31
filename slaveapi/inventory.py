from urlparse import urljoin

import requests

from . import config

def get_system(fqdn):
    url = urljoin(config["inventory_api"], "system/?format=json&hostname=%s" % fqdn)
    auth = (config["inventory_username"], config["inventory_password"])
    info = requests.get(url, auth=auth).json()["objects"][0]

    # We do some post processing because PDUs are buried in the key/value store
    # for some hosts.
    for key, value in [(i["key"],i["value"]) for i in info["key_value"]]:
        if key == "system.pdu.0":
            pdu, pdu_port = value.split(":")
            if not pdu.endswith(".mozilla.com"):
                pdu += ".mozilla.com"
            info["pdu_fqdn"] = pdu
            info["pdu_port"] = pdu_port
            break
    else:
        info["pdu_fqdn"] = None
        info["pdu_port"] = None

    return info
