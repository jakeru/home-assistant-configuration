#!/usr/bin/env python3

# Written by Jakob Ruhe in October 2020.
# This was first used 2020-10-31 Saturday with great success.
# Next year we will improve it.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import random

MOTION="binary_sensor.outdoor_motion"

OUTDOOR_LIGHTS=["switch.attic_window_lights",
                "light.outdoor_driveway",
                "light.outdoor_front",
                "light.outdoor_back_and_plugin",
                "light.hue_white_lamp_1",
                "light.hue_white_lamp_2",
                "light.outdoor_ledstrip"]

TWINKLY_LIGHTS="light.twinkly_lights"

INDOOR_LIGHTS=["switch.livingroom_plugs",
               "light.livingroom_dimmers"]

MEDIA_PLAYER="media_player.matrum"

class Halloween(hass.Hass):
    def initialize(self):
        self.have_visitors = False
        self.listen_state(self.on_motion_change, MOTION)

    def is_enabled(self):
        today = self.date()
        return today.month == 10 and today.day == 31

    def on_motion_change(self, entity, attribute, old, new, kwargs):
        self.log(
            "on_motion_change entity {} attribute {} old {} new {}".format(
                    entity, attribute, old, new))
        if not self.is_enabled():
            self.log("Halloween automation not enabled. No action taken")
            return
        if self.have_visitors:
            self.log("Already have visitors. No action taken")
            return
        self.have_visitors = True
        self.welcome_visitors()

    def welcome_visitors(self):
        self.turn_lights_off()
        self.run_in(self.welcome_step2, 3)

    def welcome_step2(self, kwargs):
        self.sound_on()
        self.run_in(self.welcome_step3, 3)

    def welcome_step3(self, kwargs):
        self.log("Turning on twinkly lights")
        self.turn_on(TWINKLY_LIGHTS)
        self.run_in(self.welcome_step4, 30)

    def welcome_step4(self, kwargs):
        self.log("Turning on outdoor_back_and_plugin")
        self.turn_on("light.outdoor_back_and_plugin")
        self.run_in(self.goodbye, 120)

    def goodbye(self, kwargs):
        self.log("Goodbye")
        self.turn_off(TWINKLY_LIGHTS)
        self.turn_lights_on()
        self.sound_off()
        self.have_visitors = False

    def turn_lights_off(self):
        self.log("Turning off lights")
        self.turn_off(TWINKLY_LIGHTS)
        for e in OUTDOOR_LIGHTS:
            self.turn_off(e)
        for e in INDOOR_LIGHTS:
            self.turn_off(e)

    def turn_lights_on(self):
        self.log("Turning on lights")
        for e in OUTDOOR_LIGHTS:
            self.turn_on(e)
        for e in INDOOR_LIGHTS:
            self.turn_on(e)

    def sound_on(self):
        self.log("Playing sound")
        self.call_service("media_player/play_media",
                          entity_id=MEDIA_PLAYER,
                          media_content_type="url",
                          media_content_id="https://www.jrteknikkonsult.se/halloween/Rain-and-rolling-thunder-sounds.mp3")
    def sound_off(self):
        self.log("Stop sound")
        self.call_service("media_player/media_stop",
                          entity_id=MEDIA_PLAYER)
