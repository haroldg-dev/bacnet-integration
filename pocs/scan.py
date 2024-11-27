from BACpypes.app import BIPSimpleApplication
from BACpypes.local.device import LocalDeviceObject
from BACpypes.pdu import Address
from BACpypes.netservice import NetworkServiceAccessPoint, NetworkServiceElement
from BACpypes.service.device import WhoIsIAmServices

# Configuration for the local BACnet device
device_config = {
    'objectName': 'Python-BACnet-Device',
    'objectIdentifier': 12345,
    'maxApduLengthAccepted': 1024,
    'segmentationSupported': 'segmentedBoth',
    'vendorIdentifier': 15,
}

class BACnetApplication(BIPSimpleApplication, WhoIsIAmServices):
    def __init__(self, local_device, address):
        BIPSimpleApplication.__init__(self, local_device, address)
        WhoIsIAmServices.__init__(self)

# Define a local BACnet device
local_device = LocalDeviceObject(
    objectName=device_config['objectName'],
    objectIdentifier=device_config['objectIdentifier'],
    maxApduLengthAccepted=device_config['maxApduLengthAccepted'],
    segmentationSupported=device_config['segmentationSupported'],
    vendorIdentifier=device_config['vendorIdentifier'],
)

# BACnet IP address (broadcast)
address = Address('192.168.1.255')  # Replace with your subnet broadcast address

# Instantiate the application
bacnet_app = BACnetApplication(local_device, address)

# Network service access point
nsap = NetworkServiceAccessPoint()
nsap.bind(bacnet_app, NetworkServiceElement())

# Function to handle discovered devices
def who_is_callback(device, address):
    print(f"Discovered Device: {device} at {address}")

# Assign the callback
bacnet_app.who_is_callback = who_is_callback

# Send a Who-Is broadcast to discover devices
print("Sending Who-Is...")
bacnet_app.who_is()
