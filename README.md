# gpio-polling

Periodically poll a specified gpio pin on a Raspberry Pi and print when and what it changed to.
Can specify pin, polling period, pin pull up/down, inverted output.
A new instance will start by printing out current time and state.
Periodically poll a specified GPIO input and output whenever a change has been noticed.\nEach time program starts, the current state is printed along with 'start'

The gpio-pollingd.sh is an example of an init.d script which runs gpio-polling as daemons on startup for various pins and outputs to a timestamped file for that instance.

**dependancies:**

RPi.GPIO python module

**usage**

gpio_polling.py [-h] -p PIN [-T PERIOD] [-P PUD] [-i]

arguments:
  -h, --help            show this help message and exit
  -p PIN, --pin PIN     GPIO pin to poll
  -T PERIOD, --period PERIOD
                        polling period in seconds. default 10s.
  -P PUD, --pud PUD     set pin pull up/down. -1, 0, 1 for pull down, off, up. default 0.
  -i, --invert          invert output. default false.

**usage example**:

gpio-polling -p17 >> pin17.log

Had tried using interupts driven by a Schmitt trigger but was still getting false readings so ended up using polling method.
Setup with current sensor clamp on a wire running to hot water heater and used a comparitor and a Schmitt trigger buffer to sense when the thermostat turned on and off. 

**setup**
if running as daemon, edit gpio_pollingd to specific needs.
	make sure scripts have execute permissions.
sudo chmod 755 gpio-polling.py gpio-pollingd.sh
	copy scripts over to appropriate locations:
sudo cp gpio-polling.py /usr/local/bin/gpio-polling
sudo cp gpio-pollingd.sh /etc/init.d/gpio-pollingd
	register script at startup:
sudo update-rc.d gpio-pollingd defaults

	un-register script at startup:
sudo update-rc.d -f  gpio-pollingd remove  
