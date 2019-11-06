import appdaemon.plugins.hass.hassapi as hass
import datetime

BINARY_SENSOR="binary_sensor.guestroom_motion"
LIGHT="light.guest_toilet"

class Guestroom(hass.Hass):
    def initialize(self):
        self.listen_state(self.on_state_change, BINARY_SENSOR)
    def is_night(self):
        morning = datetime.time(hour=5, minute=30)
        night = datetime.time(hour=22, minute=30)
        now = datetime.datetime.now().time()
        return now < morning or now >= night
    def on_state_change(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Guestroom: Turning on light, is_night: {}, sun_down: {}".format(self.is_night(), self.sun_down()))
            if self.is_night() and self.sun_down():
                self.turn_on(LIGHT, brightness_pct=1)
            else:
                self.turn_on(LIGHT, brightness_pct=100)
        else:
            self.log("Guestroom: Turning off light")
            self.turn_off(LIGHT)
