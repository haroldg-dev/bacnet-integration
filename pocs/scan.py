from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject
from bacpypes.pdu import Address
from bacpypes.netservice import NetworkServiceAccessPoint, NetworkServiceElement
from bacpypes.service.device import WhoIsIAmServices

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

# BACnet IP address and port (adjust for your network)
address = Address('192.168.1.75:47800')  # Replace with your actual IP:port

# Instantiate the BACnet application
bacnet_app = BACnetApplication(local_device, address)

# Network Service Access Point (NSAP)
nsap = NetworkServiceAccessPoint()

# Network Service Element (NSE)
nse = NetworkServiceElement()

# Bind NSE and BACnet application to the NSAP
nsap.bind(nse, bacnet_app)

# Function to handle discovered devices
def who_is_callback(device, address):
    print(f"Discovered Device: {device} at {address}")

# Assign the callback
bacnet_app.who_is_callback = who_is_callback

# Send a Who-Is broadcast to discover devices
print("Sending Who-Is...")
bacnet_app.who_is()
