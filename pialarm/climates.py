from requests import post
import json


class Climates:
    def __init__(self, token, entities, host="localhost"):
        self.token = token
        self.entities = entities
        self.host = host

    def switch(self, state):
        state = "heat" if state == "on" else "off"
        response = post(
            f"http://{self.host}:8123/api/services/climate/set_hvac_mode",
            headers={
                "Authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            },
            data=json.dumps({"entity_id": self.entities, "hvac_mode": state}),
        )

        return response.status_code == 200
