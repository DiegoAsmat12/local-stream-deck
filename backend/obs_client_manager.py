import os
import threading
import logging

from dotenv import load_dotenv
import obsws_python as obs


load_dotenv()
logger = logging.getLogger("obs")

class OBSClientManager:
    def __init__(self) -> None:
        self.host = os.getenv("OBS_HOST", "localhost")
        self.port = int(os.getenv("OBS_PORT", 4455))
        self.password = os.getenv("OBS_PASSWORD", "")
        self._client: obs.ReqClient | None = None
        

    def connect(self) -> obs.ReqClient:
        if self._client is None:
            self._client = obs.ReqClient(
                host = self.host,
                port = self.port,
                password = self.password,
                timeout = 5
            )

        return self._client

    def disconnect(self):

        # Y que pasa si el cliente esta desconectado
        if self._client is not None:
            try:
                self._client.disconnect()
                logger.info("OBS Connection closed")
            finally:
                self._client = None

    def get_client(self) -> obs.ReqClient:
        if self._client is None:
            return self.connect()
        return self._client

    # Limpiar el cliente
    def reset(self) -> None:
        self._client = None


    #Sistema de Reintentos


obs_manager = OBSClientManager()


if __name__ == "__main__":
    client = obs_manager.get_client()

    scene = client.get_current_program_scene()


    name = scene.scene_name
    item_list = client.get_scene_item_list(name)

    print("Scene is: " + str([s['sourceName'] for s in item_list.scene_items]))

    obs_manager.disconnect()

    ## COMO MIERCOLES LLEGAMOS A LAS SCENES de VERTICAL

