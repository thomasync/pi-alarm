from alarm.alarm import Alarm
from alarm.config import Config

config = Config()

alarm = Alarm(
    fadein=config.fadein,
    max_duration_sound=config.max_duration_sound,
    default_volume=config.default_volume,
    maximum_volume=config.maximum_volume,
    insane_mode_delay=config.insane_mode_delay,
)
