# freezer.py

# Written by Jakob Ruhe July 2020.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import random

import config

# List of services to notify.
NOTIFY = ["notify/mobile_app_jabbe"]

class Freezer(hass.Hass):
    def initialize(self):
        self.first_bad_value_at = None
        self.last_alarm_at = None
        self.entity = self.args["entity"]
        self.max_value = float(self.args["max_value"])
        self.max_time = int(self.args["max_time"])
        self.run_every(self.on_periodic_check, datetime.datetime.now(), 60)
        self.log("Initialized for entity {}, max_value: {}, max_time: {}".format(self.entity, self.max_value, self.max_time))

    def on_periodic_check(self, kwargs):
        try:
            value = float(self.get_state(self.entity))
        except (ValueError, TypeError):
            value = None
        if value is None or value > self.max_value:
            self.handle_bad_value(value)
        else:
            self.handle_ok_value(value)

    def notify(self, title, msg):
        self.log("Notifying {}, title: {}, message: {}".format(NOTIFY, title, msg))
        for n in NOTIFY:
            self.call_service(n, title=title, message=msg)

    def handle_bad_value(self, value):
        if self.last_alarm_at is not None:
            return
        now = datetime.datetime.now()
        if self.first_bad_value_at is None:
            self.log("Bad value detected: {}".format(value))
            self.first_bad_value_at = now
            return
        minutes = (now - self.first_bad_value_at).total_seconds() / 60
        if minutes < self.max_time:
            return
        self.raise_alarm(value)

    def handle_ok_value(self, value):
        if self.last_alarm_at is not None:
            self.cancel_alarm(value)
        elif self.first_bad_value_at is not None:
            self.log("OK value detected, no alarm raised: {}".format(value))
            self.first_bad_value_at = None

    def raise_alarm(self, value):
        self.last_alarm_at = datetime.datetime.now()
        self.notify("Warning", "Bad value detected for entity {}: {}".format(self.entity, value))

    def cancel_alarm(self, value):
        self.last_alarm_at = None
        minutes = (datetime.datetime.now() - self.first_bad_value_at).total_seconds() / 60
        self.notify("Restored", "After {} minutes, entity {} is back to normal: {}".format(minutes, self.entity, value))
