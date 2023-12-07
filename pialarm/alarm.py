import os
import random
import threading
import time
import datetime
from glob import glob
from os import environ
from pialarm.utils import Utils
import re

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame import mixer


from pygame import mixer
import os
import random
import threading
import time
import datetime


class Alarm:
    def __init__(
        self,
        fadein=False,
        max_duration_sound=None,
        default_volume=50,
        maximum_volume=90,
        insane_mode_delay=None,
        lights=None,
    ):
        self._max_duration_sound = None
        self._fadein = fadein
        self._default_volume = None
        self._maximum_volume = None
        self._insane_mode_delay = None

        self.default_volume = default_volume
        self.maximum_volume = maximum_volume
        self.max_duration_sound = max_duration_sound
        self.insane_mode_delay = insane_mode_delay
        self.lights = lights

        self.__sounds = []
        self.__last_play = None
        self.__stopped = False
        self.__mode_insane = False
        self.__first_sound = True
        self.__hour = None
        self.__thread = None

        self.__clock()

    @property
    def max_duration_sound(self):
        return self._max_duration_sound

    @max_duration_sound.setter
    def max_duration_sound(self, value):
        if not value or value <= 0:
            self._max_duration_sound = None
        else:
            self._max_duration_sound = value

    @property
    def default_volume(self):
        return self._default_volume

    @property
    def default_volume(self):
        return self._default_volume

    @default_volume.setter
    def default_volume(self, value):
        if not value or value <= 0:
            self._default_volume = 0
        elif self.maximum_volume is not None and value > self.maximum_volume:
            self._default_volume = self.maximum_volume
        elif value > 100:
            self._default_volume = 100
        else:
            self._default_volume = value

    @property
    def maximum_volume(self):
        return self._maximum_volume

    @maximum_volume.setter
    def maximum_volume(self, value):
        if not value or value <= 0:
            self._maximum_volume = 0
        elif value < self.default_volume:
            self._maximum_volume = self.default_volume
        elif value > 100:
            self._maximum_volume = 100
        else:
            self._maximum_volume = value

    @property
    def insane_mode_delay(self):
        return self._insane_mode_delay

    @insane_mode_delay.setter
    def insane_mode_delay(self, value):
        if not value or value <= 0:
            self._insane_mode_delay = None
        else:
            self._insane_mode_delay = value

    @property
    def hour(self):
        return self.__hour

    @property
    def sounds(self):
        return self.__sounds

    @hour.setter
    def hour(self, value):
        if not value or not re.match(r"\d{2}:\d{2}", value):
            raise ValueError("Invalid hour format")

        hour, minute = value.split(":")
        if int(hour) > 23 or int(minute) > 59:
            raise ValueError("Invalid hour format")

        self.__hour = value

    def play(self):
        if self.__thread:
            Utils.log("[play] alarm already running")
            return

        if (
            self.__last_play
            and datetime.datetime.now() - self.__last_play
            < datetime.timedelta(minutes=2)
        ):
            Utils.log("[play] alarm already played")
            return

        if self.lights:
            Utils.log("[play] lights on")
            self.lights.switch("on")

        self.__last_play = datetime.datetime.now()
        self.__sounds = self.get_sounds()
        sounds_formatted = self.format_sounds(self.__sounds, "text")
        Utils.log(
            "[load] sounds({}): \n\t{}".format(len(self.__sounds), sounds_formatted)
        )

        self.__thread = threading.Thread(
            target=self.__play_sounds, args=(self.__sounds,)
        )
        self.__thread.start()

    def stop(self):
        if not self.__thread:
            Utils.log("[stop] alarm not running")
            return

        Utils.log("[stop] alarm stopping")

        if self.__thread:
            self.__stopped = True
            self.__thread.join()
            self.__thread = None

    def get_sounds(self, randomize=True):
        sounds_path = os.path.join(os.path.dirname(__file__), "..", "sounds")
        sounds = glob(os.path.join(sounds_path, "*.mp3"))
        if randomize:
            random.shuffle(sounds)
        return sounds

    def format_sounds(self, sounds, type_format="text"):
        sounds = [os.path.basename(sound) for sound in sounds]

        if type_format == "html":
            return "<br>".join([os.path.basename(sound) for sound in sounds])
        elif type_format == "text":
            return "\n\t".join([os.path.basename(sound) for sound in sounds])
        else:
            return sounds

    def get_duration_from_alarm_start(self):
        if not self.hour or not self.__thread:
            return 0

        date = datetime.datetime.now()
        date_alarm = datetime.datetime.strptime(
            "{} {}".format(date.date(), self.hour), "%Y-%m-%d %H:%M"
        )

        delta_seconds = (date - date_alarm).total_seconds()

        if delta_seconds < 0:
            return 0

        return delta_seconds

    def get_delay_before_alarm(self, with_seconds=True):
        if not self.hour:
            return 0

        date = datetime.datetime.now()
        date_alarm = datetime.datetime.strptime(
            "{} {}".format(date.date(), self.hour), "%Y-%m-%d %H:%M"
        )

        delta_seconds = (date_alarm - date).total_seconds()

        if delta_seconds < 0:
            date_alarm = date_alarm + datetime.timedelta(days=1)
            delta_seconds = (date_alarm - date).total_seconds()

        return Utils.format_seconds(delta_seconds, with_seconds)

    def activate_insane_mode(self):
        self.__mode_insane = True
        Utils.log("[insane] enable insane mode")

        volume = self.default_volume
        while volume < self.maximum_volume and not self.__stopped:
            volume += 1
            Utils.setVolume(volume)
            Utils.log("[insane] volume: {}".format(volume))
            time.sleep(1)

    def __clock(self):
        hour = time.strftime("%H:%M")
        if not self.__thread and self.hour and self.hour == hour:
            self.play()

        if (
            not self.__mode_insane
            and self.insane_mode_delay
            and self.get_duration_from_alarm_start() > self.insane_mode_delay
        ):
            self.activate_insane_mode()

        threading.Timer(30, self.__clock).start()

    def __play_sounds(self, sounds):
        self.__stopped = False
        self.__first_sound = True
        self.__mode_insane = False
        Utils.setVolume(self.default_volume)

        Utils.log("[play] nb sounds: {}".format(len(sounds)))

        while sounds and not self.__stopped:
            if self.__first_sound:
                self.__play_sound(sounds[0], True)
                self.__first_sound = False
            else:
                self.__play_sound(sounds[0], False)

            sounds.pop(0)

        self.__thread = None

    def __play_sound(self, sound, fade_in):
        Utils.log(
            "[play] sound: {}, fade_in: {}, max_duration_sound: {}".format(
                os.path.basename(sound),
                fade_in,
                self.max_duration_sound if self.max_duration_sound else "None",
            )
        )

        mixer.init()
        mixer.music.load(sound)

        mixer.music.play()

        if fade_in and self._fadein:
            self.__fadein(0.1, 1, 0.05)
        else:
            mixer.music.set_volume(1)

        last_time = time.time()
        breaked = False
        while mixer.music.get_busy():
            duration = round(mixer.music.get_pos() / 1000)
            if time.time() - last_time > 5:
                Utils.log(
                    "[play] duration: {} / total_duration: {}".format(
                        duration, self.get_duration_from_alarm_start()
                    )
                )
                last_time = time.time()

            if self.max_duration_sound and duration > self.max_duration_sound:
                Utils.log("[stop] max_duration_sound reached")
                breaked = True
                break

            if self.__stopped:
                Utils.log("[stop] stop sound")
                breaked = True
                break

        if not breaked:
            Utils.log("[stop] sound finished")

        mixer.quit()

    def __fadein(self, start_volume=0.1, end_volume=1.0, increment=0.05, duration=2):
        Utils.log("[fadein] start")

        while mixer.music.get_busy() and start_volume < end_volume:
            start_volume += increment
            mixer.music.set_volume(start_volume)
            Utils.log("[fadein] set volume: {}".format(start_volume))

            time.sleep(duration)

        Utils.log("[fadein] end")
