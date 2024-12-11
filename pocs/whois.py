# import asyncio
# import BAC0

# async def main():
#     bacnet = BAC0.connect(ip="10.10.5.177/24", port=47809)

#     await bacnet.who_is()
#     devices = await bacnet.devices
#     print(devices)

# # Run the main function asynchronously
# if __name__ == "__main__":
#     asyncio.run(main())

# curl 'http://10.10.5.56/cgi-bin/mdacxml.cgi?req=devsta&devid=indoor-2-4&ttt=1732991527347'

import asyncio
from bacpypes3.app import Application
from bacpypes3.local.device import DeviceObject
from bacpypes3.pdu import Address

async def main():
    # Define the local device object
    local_device = DeviceObject(
        objectIdentifier=('device', 1234),
        objectName='Local Device',
        maxApduLengthAccepted=1024,
        segmentationSupported='segmentedBoth',
        vendorIdentifier=7
    )

    # Create the application
    app = Application(local_device, Address('10.10.5.177/24'))

    # Send a Who-Is request and await responses
    i_am_responses = await app.who_is()

    # Print discovered devices
    for response in i_am_responses:
        print(f"Device ID: {response.iAmDeviceIdentifier}, Address: {response.pduSource}")

# Run the main function
asyncio.run(main())