import appdaemon.plugins.hass.hassapi as hass
import random

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

class EntityDimAtEvening(Entity):
    def evening(self):
        self.turn_on(brightness_pct=25)

class EntityDimAtEveningFixedColor(Entity):
    def morning(self):
        self.turn_on(brightness_pct=100, hs_color=[197,77])
    def afternoon(self):
        self.turn_on(brightness_pct=100, hs_color=[255,100])
    def evening(self):
        self.turn_on(brightness_pct=25, hs_color=[285, 84])

class EntityRandomColor(Entity):
    def morning(self):
        self.turn_on(hs_color=[random.randint(0,359), random.randint(90,100)])
    def afternoon(self):
        self.turn_on(hs_color=[random.randint(0,359), random.randint(90,100)])
    def evening(self):
        self.turn_on(hs_color=[random.randint(0,359), random.randint(90,100)])

class Scenes(hass.Hass):
    def initialize(self):
        self.current_scene = None
        self.entities = [
            Entity(self, 'light.livingroom_plugs'),
            Entity(self, 'light.livingroom_dimmers'),
            EntityRandomColor(self, 'light.aeotec_zw098_led_bulb_level'),
            EntityDimAtEveningFixedColor(self, 'light.hue_color_candle_1'),
            EntityDimAtEvening(self, 'light.hue_ambiance_lamp_1'),
        ]
        self.listen_event(self.on_call_service, "call_service")
    def activate(self, scene):
        self.log("Going from scene {} to: {}".format(self.current_scene, scene))
        self.current_scene = scene
        for e in self.entities:
            e.activate_scene(scene)
    def on_call_service(self, event, data, kwargs):
        if data.get("domain") == "scene":
            scene = data["service_data"]["entity_id"]
            self.activate(scene.replace("scene.", ""))
