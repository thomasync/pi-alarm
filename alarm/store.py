from alarm.alarm import Alarm
from alarm.config import Config
from alarm.lights import Lights

config = Config()

if config.home_lights and config.home_token and config.home_url:
    lights = Lights(
        token=config.home_token,
        entities=config.home_lights,
        host=config.home_url,
    )
else:
    lights = None


alarm = Alarm(
    fadein=config.fadein,
    max_duration_sound=config.max_duration_sound,
    default_volume=config.default_volume,
    maximum_volume=config.maximum_volume,
    insane_mode_delay=config.insane_mode_delay,
    lights=lights,
)
