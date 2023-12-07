import platform, os, random, string
from glob import glob
from subprocess import call
from pialarm.config import Config


config = Config()


class Utils:
    @staticmethod
    def get_random_challenge():
        challenges_path = os.path.join(os.path.dirname(__file__), "..", "challenges")
        challenges = glob(os.path.join(challenges_path, "*.html"))
        challenge = os.path.basename(random.choice(challenges))

        return Utils.get_challenge(challenge)

    @staticmethod
    def get_challenge(challenge):
        global config
        challenges_path = os.path.join(os.path.dirname(__file__), "..", "challenges")
        index_content = open(challenges_path + "/index", "r").read()
        index_content = index_content.replace("{{token}}", config.token)

        challenge_content = open(challenges_path + "/" + challenge, "r").read()
        challenge_content = challenge_content.replace("{{name}}", config.name)

        if config.allow_phone:
            index_content = index_content.replace(
                '<div id="blocked" class="fullscreen"></div>', ""
            )

        index_content = index_content.replace(
            '<section id="alarm"></section>',
            f'<section id="alarm">{challenge_content}</section>',
        )

        return index_content

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
