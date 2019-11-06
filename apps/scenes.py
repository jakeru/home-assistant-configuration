import appdaemon.plugins.hass.hassapi as hass
import random
import time

class Entity:
    def __init__(self, api, entity_id):
        self.api = api
        self.entity_id = entity_id
    def turn_on(self, **kwargs):
        self.api.turn_on(self.entity_id, **kwargs)
    def turn_off(self, **kwargs):
        self.api.turn_off(self.entity_id, **kwargs)
    def activate_scene(self, scene):
        if scene == 'morning':
            self.morning()
        elif scene == 'day':
            self.day()
        elif scene == 'afternoon':
            self.afternoon()
        elif scene == 'evening':
            self.evening()
        elif scene == 'night':
            self.night()
    def morning(self):
        self.turn_on()
    def day(self):
        self.turn_off()
    def afternoon(self):
        self.turn_on()
    def evening(self):
        self.turn_on()
    def night(self):
        self.turn_off()

class EntityOffAtNight(Entity):
    """ Turn off the entity at night. No other actions taken. """
    def morning(self):
        pass
    def day(self):
        pass
    def afternoon(self):
        pass
    def evening(self):
        pass
    def night(self):
        self.turn_off()

class EntityDim(Entity):
    def morning(self):
        self.turn_on(brightness_pct=100)
    def afternoon(self):
        self.turn_on(brightness_pct=100)
    def evening(self):
        self.turn_on(brightness_pct=100)

class EntityDimAtEvening(EntityDim):
    def evening(self):
        self.turn_on(brightness_pct=50)

class EntityDimAtEveningFixedColor(Entity):
    def morning(self):
        self.turn_on(brightness_pct=100, hs_color=[29,71])
    def afternoon(self):
        self.turn_on(brightness_pct=100, hs_color=[29,71])
    def evening(self):
        self.turn_on(brightness_pct=50, hs_color=[29, 71])

class EntityRandomColor(Entity):
    def morning(self):
        self.turn_on(brightness_pct=100, hs_color=[random.randint(0,359), random.randint(90,100)])
    def afternoon(self):
        self.turn_on(brightness_pct=100, hs_color=[random.randint(0,359), random.randint(90,100)])
    def evening(self):
        self.turn_on(brightness_pct=25, hs_color=[random.randint(0,359), random.randint(90,100)])

class Scenes(hass.Hass):
    def initialize(self):
        self.current_scene = None
        self.last_button_pressed = None
        self.entities = [
            Entity(self, 'light.livingroom_plugs'),
            EntityDim(self, 'light.livingroom_dimmers'),
            EntityDimAtEveningFixedColor(self, 'light.aeotec_zw098_led_bulb_level'),
            EntityDimAtEveningFixedColor(self, 'light.hue_color_candle_1'),
            EntityDimAtEvening(self, 'light.hue_ambiance_lamp_1'),
            EntityOffAtNight(self, 'light.playroom'),
        ]
        self.listen_event(self.on_call_service, "call_service")
        self.listen_event(self.on_button_pressed, "button_pressed")
    def activate(self, scene):
        self.log("Going from scene {} to: {}".format(self.current_scene, scene))
        self.current_scene = scene
        for e in self.entities:
            e.activate_scene(scene)
    def on_call_service(self, event, data, kwargs):
        if data.get("domain") == "scene":
            scene = data["service_data"]["entity_id"]
            if isinstance(scene, list):
                scene = scene[0]
            self.activate(scene.replace("scene.", ""))
    def on_button_pressed(self, event, data, kwargs):
        self.log("on_button_pressed: {}, data: {}, kwargs: {}".format(event, data, kwargs))
        if data["entity_id"] != "switch.hall":
            return
        if self.last_button_pressed is not None and time.time() - self.last_button_pressed < 0.1:
            return
        self.last_button_pressed = time.time()
        if data["state"] == "off":
            scene = "night"
        elif self.current_scene == "evening":
            scene = "afternoon"
        elif self.current_scene == "afternoon":
            scene = "morning"
        else:
            scene = "evening"
        self.activate(scene)
