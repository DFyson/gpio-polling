#!/bin/bash
#/etc/init.d/gpio-pollingd

# Description:
# Daemon script for controlling gpio-polling which periodically polls GPIO pins.

# History:
# 2015-09-21: created (Devon Fyson)

# Refs:
# http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html
# http://werxltd.com/wp/2012/01/05/simple-init-d-script-template/

# TODO:
# use test when executing

### BEGIN INIT INFO
# Provides:          gpio-pollingd
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: gpio-pollingd
# Description:       Script for periodically polling a GPIO pin and spitting out timestamp.
### END INIT INFO

script=/usr/local/bin/gpio-polling
pidfile=/var/run/gpio-pollingd.pid

test -x $script || (echo "$scipt non existant or wrong permissions." & exit 0) #make sure script actually exists.

# Carry out specific functions when asked to by the system
case "$1" in
	start)
		#ensure process not already running.
		if [[ -s $pidfile ]]; then #if PID file is not empty.
			echo "PID file not empty. Daemon already started? Or try stopping and starting."
			exit 1
		fi

		ts=`date +"%F_%R:%S"` #timestamp

		echo "Starting... "
		$script -p=17 >> /var/www/gpio-polling/17/17_$ts.log & #script to run
		echo $! >> $pidfile #write PID of last job run in background to PID file.
		echo "ok."

		$script -p=18 >> /var/www/gpio-polling/18/18_$ts.log &
		echo $! >> $pidfile
		echo "ok."
	;;
	stop)
		if [[ -s $pidfile ]]; then #ensure PID file has processes to kill.
			echo "Stopping..."
			kill `cat $pidfile` #kill all PIDs in PID file. Dont killall instances of the process since user may have started some non-daemon instances.
			rm $pidfile #remove PID file.
			echo "ok."
		else
			echo "PID file empty. Nothing to kill."
			exit 1
		fi
	;;
	*)
		echo "Usage: /etc/init.d/gpio-pollingd {start|stop}"
		exit 1
	;;
esac

exit 0 
