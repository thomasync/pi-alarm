import os, random, string
from dotenv import load_dotenv
import json

load_dotenv()


class Config:
    def __init__(self):
        if not os.path.isfile(".env"):
            self.__create_env_file()

        self._token = (
            os.getenv("TOKEN")
            if os.getenv("TOKEN") and os.getenv("TOKEN") != "None"
            else self.__generate_token()
        )

    @property
    def token(self):
        return self._token

    @property
    def name(self):
        return os.getenv("NAME", "John Doe")

    @property
    def debug(self):
        return (
            os.getenv("DEBUG") == "True"
            or os.getenv("DEBUG") == "true"
            or os.getenv("DEBUG") == "1"
        )

    @property
    def fadein(self):
        return (
            os.getenv("FADEIN") == "True"
            or os.getenv("FADEIN") == "true"
            or os.getenv("FADEIN") == "1"
        )

    @property
    def max_duration_sound(self):
        return (
            None
            if os.getenv("MAX_DURATION_SOUND") == "None"
            else int(os.getenv("MAX_DURATION_SOUND", 60))
        )

    @property
    def default_volume(self):
        return int(os.getenv("DEFAULT_VOLUME", 50))

    @property
    def maximum_volume(self):
        return int(os.getenv("MAXIMUM_VOLUME", 90))

    @property
    def insane_mode_delay(self):
        return (
            None
            if os.getenv("INSANE_MODE_DELAY") == "None"
            else int(os.getenv("INSANE_MODE_DELAY", 60))
        )

    @property
    def home_url(self):
        return os.getenv("HOME_URL")

    @property
    def home_lights(self):
        lights = json.loads(os.getenv("HOME_LIGHTS"))
        return lights if lights and len(lights) > 0 else None

    @property
    def home_token(self):
        return os.getenv("HOME_TOKEN")

    def __generate_token(self):
        token = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(32)
        )

        env = open(".env", "r").read()
        env = env.replace("TOKEN=None", "TOKEN={}".format(token))

        with open(".env", "w") as file:
            file.write(env)

        return token

    def __create_env_file(self):
        env_example = open(".env.example", "r").read()
        with open(".env", "w") as file:
            file.write(env_example)
