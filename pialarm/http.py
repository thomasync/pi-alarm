from http.server import BaseHTTPRequestHandler
import re
from pialarm.store import alarm, config
from pialarm.utils import Utils
from pialarm import __version__
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global alarm, config
        code = 200
        is_json = False
        content = None

        # Verify the token
        authentified = self.headers.get("Authorization") == config.token

        try:
            if authentified and re.match(r"/set/\d{2}:\d{2}", self.path):
                hour = self.path.split("/")[-1]
                alarm.hour = hour
                content = "{} ({})".format(hour, alarm.get_delay_before_alarm(False))

            elif authentified and self.path == "/stop":
                alarm.stop()
                content = "alarm stopped"

            elif authentified and self.path == "/infos":
                json_data = alarm.__dict__.copy()
                del json_data["_Alarm__thread"]
                del json_data["lights"]
                del json_data["_Alarm__last_play"]
                json_data["duration"] = alarm.get_duration_from_alarm_start()
                json_data["delay"] = alarm.get_delay_before_alarm()
                json_data["_Alarm__sounds"] = alarm.format_sounds(alarm.sounds, "json")
                json_data["sounds"] = alarm.format_sounds(
                    alarm.get_sounds(False), "json"
                )
                json_data["version"] = __version__
                content = json.dumps(json_data)
                is_json = True

            elif self.path == "/{}".format(config.token):
                content = Utils.get_random_challenge()

            # elif self.path == "/test_challenge":
            #     content = Utils.get_challenge("bubbles.html")

            else:
                code = 404
                content = "unknown path"

        except Exception as e:
            code = 500
            content = "error: {}".format(str(e))

        self.send_response(code)

        if is_json:
            self.send_header("Content-type", "application/json")
        else:
            self.send_header("Content-type", "text/html")

        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))
