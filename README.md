Since 2012 I have a several Nexa sensors and switches which are still
working well. I used a Raspberry Pi 2 and a Tellstick Duo at that time.
I experimented for a while with different libraries and applications.

The Tellstick Duo stopped working after a while and there was not too much
to automate in the apartment anyway so I pasued the home automation idea until
we moved into a house early 2016.

In early October 2016 I bought some stuff and started playing with Home Automation
which looked very promising.

Equipment:

- Raspberry Pi 3 running Raspbian
- RFXtrx433E USB 433.92 MHz Tranceiver
- Aeon Labs Z-Stick (Gen 5)
- Fibaro Motion Sensor (4 in 1, Gen 5)
- 3 temperature/humidity sensors (433.92 MHz)
- A bunch of 433.92 MHz Nexa switches
- A few Z-wave switches
- A wall mounted iPad to control stuff
- HEOS sound system (not controlled by Home Assistant yet)

Automations today:

- Indoor lights on during morning and evening.
- Outdoor lights on when sun is down.
- Lights in playroom are switched on when motion is detected. 10 minutes
  after the Fibaro Motion sensor reports no motion, the lights are
  switched off.

More plans:
- I have 4 IP cameras which I want to include in Home Assistant.
- I want to include my HEOS by Denon devices into Home Assistant.

