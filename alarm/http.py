from http.server import BaseHTTPRequestHandler
import re
from alarm.store import alarm, config
from alarm.utils import Utils
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global alarm, config
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # Verify the token
        authentified = self.headers.get("Authorization") == config.token

        try:
            if authentified and re.match(r"/set/\d{2}:\d{2}", self.path):
                hour = self.path.split("/")[-1]
                alarm.hour = hour
                message = "{} ({})".format(hour, alarm.get_delay_before_alarm(False))
                self.wfile.write(bytes(message, "utf8"))

            elif authentified and self.path == "/stop":
                alarm.stop()
                self.wfile.write(bytes("alarm stopped", "utf8"))

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
                self.wfile.write(bytes(json.dumps(json_data), "utf8"))

            elif self.path == "/{}".format(config.token):
                self.wfile.write(bytes(Utils.get_random_challenge(), "utf8"))

            else:
                raise Exception("unknown path")

        except Exception as e:
            self.wfile.write(bytes("error: {}".format(str(e)), "utf8"))
