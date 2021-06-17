from django.shortcuts import render
from ncclient import manager
import xmltodict
import xml.dom.minidom


def main(interfaces):
    always_csr = {"host": "ios-xe-mgmt.cisco.com",
                  "username": "developer",
                  "password": "C1sco12345",
                  "port": 10000,
                  "hostkey_verify": False,
                  "device_params": {"name": "csr"}}

    router = always_csr

    netconf_filter = """
    <filter>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
      </interfaces>
    </filter>"""

    with manager.connect(**router) as m:
        reply = m.get_config(source="running", filter=netconf_filter)

    # Print entire reply
    # print(xml.dom.minidom.parseString(str(reply)).toprettyxml())
    interfaces.append(xml.dom.minidom.parseString(str(reply)).toprettyxml())


    # netconf_data = xmltodict.parse(reply.xml)["rpc-reply"]["data"]

    # interfaces.append(netconf_data["interfaces"]["interface"])

    # for i in interfaces:
    #     print(f"Interface {i['name']} status is: {i['enabled']}")

    return interfaces

def interfaces(request):
    interfaces = []
    main(interfaces)

    context = {
        "interfaces": interfaces
    }
    return render(request, "netdev/interfaces.html", context)


def test(request):
    return render(request, "netdev/dev_test.html")
