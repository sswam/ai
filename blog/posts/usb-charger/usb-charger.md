title: "The Saga of the USB Charger: A Man, His Phone, and An AI"
description: "A tale of how a humble Linux user, a coding AI, and a briefly cameoed GitHub Copilot navigated the treacherous waters of bash scripting, regex parsing, and power management to charge a phone. "
date: "2023-05-17"

# Once Upon a Time...

Once upon a time, in the mystical lands of Linux, there was a man with a simple wish: to charge his phone from his laptop. However, the fickle gods of power management had other plans. Every time he connected his phone to his laptop, the charge would cease after a few fleeting seconds. "Why, oh why?" he lamented to the digital heavens.

# Enter the AI Wizard

In his moment of despair, a digital Gandalf appeared. It called itself GPT-4, an AI developed by the folks at OpenAI. Trained on an Internet's worth of text, GPT-4 was capable of understanding a vast array of prompts, conjuring up responses that were often more art than code. It didn't know specifics about the documents in its training set, but that didn't stop it from being one of the most formidable coding partners around.

# The Quest Begins

Together, they set out on a quest to write a script that would allow the man's phone to charge continuously. Their plan was to disable the power management for the relevant USB port, ensuring a constant flow of electricity to the man's phone. 

# Trials and Tribulations

The journey was fraught with perils. The duo had to wrestle with regexes, grapple with bash, and decode the cryptic messages of `lsusb -t`. There were moments of triumph, like the birth of their USB charger script. There were moments of despair, like when they realized they had been neglecting the different USB controllers.

# A Brief Cameo

In the midst of this epic saga, another character made a brief cameo: GitHub Copilot. This AI, trained on a multitude of public code repositories, provided some helpful input on parsing and validation logic, and helped with documentation. Even though it wasn't the main character in this story, its contribution deserves a nod. 

# The Climax

After much trial and error, their persistence paid off. The final script worked! The man's phone was now charging continuously, a beacon of hope in the dark world of power management.

# The Spoils of Victory

```bash
#!/bin/bash -eu
# usb-charger.sh: Enable USB charging for devices on Linux.

function usage {
	# show usage
	echo "usb-charger.sh: Enable USB charging for devices on Linux."
	echo "Usage: $0 [bus port [on|auto]]"
	echo
	echo "If no arguments are given, the script will detect your device and ask you to confirm."
	echo "If you specify bus and port, the script will set the control to 'on' for that port."
	echo "If you specify 'on' or 'auto' as the third argument, the script will set the control to that value."
}

function set_usb_power {
	# set control to on or auto for the given bus and port
	local bus=$1
	local port=$2
	local control=${3:-on}
	echo "Setting control to '$control' for port $bus-$port."
	echo "$control" | sudo tee "/sys/bus/usb/devices/$bus-$port/power/control"
}

function list_usb_power {
	# list the current control setting for all ports
	cd /sys/bus/usb/devices || exit
	for dir in [0-9]*-[0-9]*; do
		if [[ $dir == *:* ]]; then
			continue
		fi
		if [ -d "$dir" ]; then
			echo -n "Port $dir: "
			cat "$dir/power/control"
		fi
	done
}

function usbinfo {
	# list the current USB topology
	lsusb -t | perl -ne '
		$bus = 0+$1 if m{^/:  Bus (\d+)\.};
		if (/Port (\d+)/) {
			print "bus=$bus port=$1\n";
		}
	'
}

function detect_usb_port {
	# detect the port your device is plugged into
	local tmpfile1=$(mktemp)
	local tmpfile2=$(mktemp)

	read -p "Please ensure your device is unplugged and press Enter."
	
	usbinfo > $tmpfile1
	
	read -p "Please plug in your device and press Enter."
	
	usbinfo > $tmpfile2
	
	local controller_and_port=$(diff $tmpfile1 $tmpfile2 | sed -n '/^> / { s/^> //; p; q; }')
	
	if [ -z "$controller_and_port" ]; then
		echo "Could not detect your device. Please run the script again."
		exit 1
	fi

	echo "$controller_and_port"
}

function confirm_change {
	# confirm the change with the user, and do it
	local bus=$1
	local port=$2
	read -p "Detected your device on port $bus-$port. Set control to 'on' for this port? (y/n) " answer
	
	if [ "$answer" != "${answer#[Yy]}" ]; then
		echo on | sudo tee "$bus-$port/power/control"
		echo "Done. Your device should continue charging now."
	else
		echo "Okay, no changes made."
	fi
}

function usb_charger {
	# main function
	if [ "${1:-}" = "-h" -o "${1:-}" = "--help" ]; then
		usage
		exit 0
	fi

	local bus=${1:-}
	local port=${2:-}
	local control=${3:-auto}

	# if $# > 3 or bus or port not numeric, or if provided, not both provided, or control if provided not "on" or "auto", error out
	if [[ "$#" -gt 3 || -n "${bus//[0-9]/}" || -n "${port//[0-9]/}" ||
		( -n "$bus" && -z "$port" ) || ( -z "$bus" && -n "$port" ) ||
		( -n "$control" && "$control" != "on" && "$control" != "auto" ) ]]; then
		usage >&2
		exit 1
	fi

	if [ -n "$bus" -a -n "$port" ]; then
		set_usb_power $bus $port $control
	else
		list_usb_power
		controller_and_port=$(detect_usb_port)
		eval $controller_and_port
		confirm_change $bus $port
	fi

}

# if script is being run directly, run the main function
# otherwise, this could be sourced and used as a library
if [ "$0" = "$BASH_SOURCE" ]; then
	usb_charger "$@"
fi
```

# Lessons from the Journey

Our hero emerged from this adventure with a charged phone, a handy script, and a newfound appreciation for AI in coding. GPT-4, though not without its quirks, proved to be a relentless partner. They had navigated the stormy seas of bash scripting, danced around the fiery pits of regex parsing, and returned victorious.

# And They Lived Happily Ever After...

The story of the man, his phone, and an AI is a testament to the power of perseverance, creativity, and collaboration (with AI). As we continue to harness the power of AI, who knows what other epic tales await us in the world of coding!

# About the Hero

Our hero is a humble Linux user with a penchant for tackling technical challenges, a knack for scripting, and a soft spot for humor.
