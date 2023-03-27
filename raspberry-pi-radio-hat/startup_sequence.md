# Canique Radio Hat: Startup Sequence

This page provides detailed information about how Canique Radio Hat (HW rev 0.8.x) starts up.

The software package that interacts with the Canique Radio Hat is called canique-radio-bridge. It communicates with the hat using a 500kbps UART connection.

## Startup
When starting the canique-radio-bridge service, this is what happens (canique-radio-bridge: debian package version 0.8.4).

1. The service outputs "Hard resetting Gateway Hat" in the log file. Immediately after that, the RESET pin (Raspberry Pi GPIO 22) of the Hat is pulled low for 2ms - the MCU of the Hat does a reset, clears its RAM, and resets the radio controller. It's similar to a power cycle of the Hat.

2. canique-radio-bridge will now immediately drop root privileges if it has been started as root.

3. Meanwhile the Hat will run its bootloader: its RX and TX Led will blink simultaneously while the bootloader is running. The bootloader is setup to wait for up to 5 seconds for an input via UART after sending some information via UART. But in practice the bootloader will start the main application much faster because canique-radio-bridge will read the bootloader messages and send a command in response to run the main application. In case that canique-radio-bridge misses the bootloader output via UART, and does not instruct the bootloader to continue with the main application, the bootloader will do so anyway after the 5s timeout.

4. Once the main application on the Hat starts, it initializes some components on the board, and then immediately sends a "Gateway Module started up" message which you can see in the log output - canique-radio-bridge is actively waiting for this message for up to 6 seconds after resetting the Hat. If the message is not received the service will exit with an error message (error code 3): "Timed out waiting for Radio Hat to start up. Is Radio Hat connected? Exiting."

5. ...
