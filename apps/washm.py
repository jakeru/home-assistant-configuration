# washm.py

# Sends a notification when the laundry is finished using
# AppDaemon and Home Assistant.
# The power the washing machine consumes is measured using a
# Fibaro wall plug generation 5. Make sure to use a wall plug
# that can handle the amount of power the washing machine
# needs!

# Written by Jakob Ruhe 2019.

import appdaemon.plugins.hass.hassapi as hass
import datetime
import random

POWER="sensor.laundry_washing_machine_power"
ENERGY="sensor.laundry_washing_machine_energy"

# Minimum power while washing.
POWER_WASHING = 5

# Minimum power consumed when finished but not emptied.
POWER_NOT_EMPTIED = 0.5

# Possible states.
STATE_OFF = "off"
STATE_WASHING = "washing"
STATE_NOT_EMPTIED = "not-emptied"

# Number of times in a new state before actually changing state.
NUM_SAME_STATE_MIN = 10

# List of services to notify.
NOTIFY = ["notify/family"]

class WashingMachine(hass.Hass):
    def initialize(self):
        self.state = None
        self.plausable_new_state = None
        self.num_same_state = 0
        self.started_at = None
        self.energy_at_start = None
        self.finished_at = None
        self.state = None
        self.set_state("sensor.washing_machine", state="unknown", attributes={"friendly_name":"Tvättmaskinen"})
        self.run_every(self.on_periodic_check, datetime.datetime.now(), 10)
        self.listen_state(self.on_power_change, POWER)
    def on_power_change(self, entity, attribute, old, new, kwargs):
        self.log("on_power_change entity {} attribute {} old {} new {}".format(entity, attribute, old, new))
    def on_periodic_check(self, kwargs):
        try:
            power = float(self.get_state(POWER))
        except ValueError:
            return
        self.evaluate_state(power)
    def evaluate_state(self, power):
        if power >= POWER_WASHING:
            state = STATE_WASHING
        elif power >= POWER_NOT_EMPTIED:
            state = STATE_NOT_EMPTIED
        else:
            state = STATE_OFF
        if self.plausable_new_state != state:
            self.plausable_new_state = state
            self.num_same_state = 0
        else:
            self.num_same_state += 1
        if self.plausable_new_state != self.state:
            self.log("evaluate_state power {} state {} plausable_new_state {} num_same_state {}".format(power, self.state, self.plausable_new_state, self.num_same_state))
            if self.num_same_state == NUM_SAME_STATE_MIN:
                self.enter_new_state(state)
    def enter_new_state(self, state):
        prev_state = self.state
        self.log("Going from state {} to {}".format(prev_state, state))
        self.set_state("sensor.washing_machine", state=state)
        self.state = state
        if state == STATE_WASHING:
            self.started_at = datetime.datetime.now()
            self.energy_at_start = float(self.get_state(ENERGY))
        elif state == STATE_NOT_EMPTIED:
            self.finished_at = datetime.datetime.now()
            self.notify_finished_washing()
        elif state == STATE_OFF and prev_state == STATE_NOT_EMPTIED:
            self.notify_emptied()
    def notify_finished_washing(self):
        if self.started_at:
            minutes = int((self.finished_at - self.started_at).total_seconds() / 60)
        else:
            minutes = "?"

        if self.energy_at_start:
            energy_consumed = "{0:.3f}".format(float(self.get_state(ENERGY)) - self.energy_at_start)
        else:
            energy_consumed = "?"

        self.log("Washing machine finished after {} minutes. {} kWh consumed. Waiting to be emptied.".format(minutes, energy_consumed))

        titles = [
            "Tvätten längtar efter dig",
            "Tvätten behöver dig",
            "Tvätten kallar på dig",
            "Du behövs i tvättstugan",
            "Tvättmaskinen behöver hjälp",
        ]

        messages = [
            "Äntligen är tvättmaskinen klar! Det tog {} minuter och {} kWh gick åt.",
            "Nu, {} minuter senare, är jag klar med tvätten. {} kWh förbrukades.",
            "Jag tvättade allt på bara {} minuter och endast {} kWh gick åt.",
        ]

        title = titles[random.randint(0, len(titles) - 1)]
        message = messages[random.randint(0, len(messages) - 1)]

        for n in NOTIFY:
            self.call_service(n, title=title, message=message.format(minutes, energy_consumed))

    def notify_emptied(self):
        if self.finished_at:
            minutes = int((datetime.datetime.now() - self.finished_at).total_seconds() / 60)
        else:
            minutes = 0
        self.log("Washing machine emptied {} minutes after it was finished.".format(minutes))
        for n in NOTIFY:
            self.call_service(n, title="Tvättmaskin tömd",
                message="Tvättmaskinen är nu tömd, {} minut{} efter att tvätten blev klar.".format(minutes, "" if minutes == 1 else "er"))
