Since 2012 I have a several Nexa sensors and switches which are still
working well. I used a Raspberry Pi 2 and a Tellstick Duo at that time.
I experimented for a while with different libraries and applications.

The Tellstick Duo stopped working after a while and there was not too much
to automate in the apartment anyway so I paused the home automation hobby until
we moved into a house early 2016.

In October 2016 I bought some stuff and started playing with Home Assistant
which looked very promising.

Equipment:

- Server: Intel Atom media center
- RFXtrx433E USB 433.92 MHz Tranceiver
- Aeon Labs Z-Stick (Gen 5)
- Fibaro Motion Sensor (4 in 1, Gen 5)
- 3 temperature/humidity sensors (433.92 MHz)
- 3 temperature sensors for refridgerator and fridges (433 MHz)
- A bunch of 433.92 MHz Nexa switches
- A bunch of Z-wave switches
- A few Philips Hue devices
- A LED strip controlled by an ESP8266
- A Twinkly LED strip
- Arlo cameras
- A few other IP cameras
- 2 IKEA trådfri LED drivers in the kitchen
- HEOS sound system.
- The heatpump is connected through Home Assistant using a H1 Interface USB
  from [Husdata AB](http://husdata.se).
- A Raspberry Pi with a camera watching the water meter.

Automations:

- The laundry machine tells us when it is finished and how much energy that
  was consumed. A wall plug measuring the energy together
  with a [Python script using AppDaemon](apps/washm.py) is used for this.
- Indoor lights on during morning and evening.
- Outdoor lights on when sun is down.
- Lights in playroom are switched on when motion is detected. 10 minutes
  after the Fibaro Motion sensor reports no motion, the lights are
  switched off.
- In the guestroom, the Hue lights are turned on when someone enters the room.
  The lights are dimmed during night. An [AppDaemon script](apps/guestroom.py)
  is used also for this.
