# gpio-polling

Periodically poll a specified gpio pin on a Raspberry Pi and print when and what it changed to.
Can specify pin, polling period, pin pull up/down, inverted output.
A new instance will start by printing out current time and state.
Periodically poll a specified GPIO input and output whenever a change has been noticed.\nEach time program starts, the current state is printed along with 'start'

The gpio-pollingd.sh is an example of an init.d script which runs gpio-polling as daemons on startup for various pins and outputs to a timestamped file for that instance.

Had tried using interupts driven by a Schmitt trigger but was still getting false readings so ended up using polling method.
Setup with current sensor clamp on a wire running to hot water heater and used a comparitor and a Schmitt trigger buffer to sense when the thermostat turned on and off. 

For usage instructions, check head of gpio-polling.py.
