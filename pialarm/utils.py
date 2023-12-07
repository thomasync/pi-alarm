import platform, os, random, string
from glob import glob
from subprocess import call
from pialarm.config import Config


config = Config()


class Utils:
    @staticmethod
    def get_random_challenge():
        global config
        challenges_path = os.path.join(os.path.dirname(__file__), "..", "challenges")
        challenges = glob(os.path.join(challenges_path, "*.html"))
        challenge = random.choice(challenges)

        content = open(challenge, "r").read()
        content = content.replace("{{name}}", config.name)
        content = content.replace("{{token}}", config.token)

        return content

    @staticmethod
    def setVolume(volume):
        if Utils.getOS() == "macOS":
            control = 'osascript -e "set Volume {}"'.format(round(volume / 10))
        else:
            control = "amixer set 'PCM' {}%".format(volume)

        call(control, shell=True)

    @staticmethod
    def getOS():
        return "macOS" if platform.system() == "Darwin" else "Linux"

    @staticmethod
    def log(message):
        global config
        if config.debug:
            print(message)

    @staticmethod
    def format_seconds(seconds, with_seconds=True):
        hours = int(seconds // 3600)
        seconds = int(seconds % 3600)
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        if hours == 0:
            return "{:01d} minutes {:01d} secondes".format(minutes, seconds)

        if with_seconds:
            return "{:01d} heures {:01d} minutes {:01d} secondes".format(
                hours, minutes, seconds
            )
        else:
            return "{:01d} heures {:01d} minutes".format(hours, minutes)
