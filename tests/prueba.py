from uldaq import *

devices = get_daq_device_inventory(InterfaceType.USB)

print("Cantidad:", len(devices))

for device in devices:
    print(device)