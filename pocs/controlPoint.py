import asyncio
import BAC0

async def create_data(discovered_devices, network):
    devices = {}
    dataframes = {}
    for each in discovered_devices:
        name, vendor, address, device_id = each

        try:
            custom_obj_list = None  # Adjust if needed
            BAC0.log_level("debug")
            devices[name] = await BAC0.device(
                address, device_id, network, poll=0, object_list=custom_obj_list, timeout=10, retries=3
            )
            # Placeholder for `make_dataframe`
            dataframes[name] = {"example": "dataframe"}  # Replace with actual logic
        except Exception as e:
            print(f"Error processing device {name}: {e}")
    return devices, dataframes

async def main():
    # Initialize the BACnet application in an asynchronous context
    bacnet = BAC0.lite(ip="10.10.5.177/24", port=47800)

    try:
        # Manually add the known BACnet controller
        known_device = ("ControllerName", "VendorName", "10.10.5.56", 18)
        discovered_devices = [known_device]

        if discovered_devices:
            print(f"Discovered devices: {discovered_devices}")
            print("Creating DATA...")
            devices, dataframes = await create_data(discovered_devices, network=bacnet)
            print("Devices:", devices)
            print("Dataframes:", dataframes)
        else:
            print("No devices found on the network.")
    finally:
        # Cleanup resources
        print("DONEEEE")
        # bacnet.shutdown()

# Run the main function asynchronously
if __name__ == "__main__":
    asyncio.run(main())