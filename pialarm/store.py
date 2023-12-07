from pialarm.alarm import Alarm
from pialarm.config import Config
from pialarm.lights import Lights
from pialarm.climates import Climates

config = Config()

if config.home_lights and config.home_token and config.home_url:
    lights = Lights(
        token=config.home_token,
        entities=config.home_lights,
        host=config.home_url,
    )
else:
    lights = None

if config.home_climates and config.home_token and config.home_url:
    climates = Climates(
        token=config.home_token,
        entities=config.home_climates,
        host=config.home_url,
    )
else:
    climates = None


alarm = Alarm(
    fadein=config.fadein,
    max_duration_sound=config.max_duration_sound,
    default_volume=config.default_volume,
    maximum_volume=config.maximum_volume,
    insane_mode_delay=config.insane_mode_delay,
    lights=lights,
    climates=climates,
    climates_delay=config.home_climates_delay,
)
