from requests import post
import json


class Lights:
    def __init__(self, token, entities, host="localhost"):
        self.token = token
        self.entities = entities
        self.host = host

    def switch(self, state):
        response = post(
            f"http://{self.host}:8123/api/services/switch/turn_{state}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            },
            data=json.dumps({"entity_id": self.entities}),
        )

        return response.status_code == 200
