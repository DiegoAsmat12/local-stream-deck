
## BOILERPLATE PORQUE NO SE PYTHON
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time # STAP antes de borrar algo
from obs_client_manager import obs_manager


CINEMA_SCENE = "FX_CINEMA"
FADE_IN_MS = 350
FADE_OUT_MS = 3141 # PI?!?!

FADE_OUT_FRAMES = 40 # 40FPS

DEFAULT_TRANSITION_DURATION = 300

def run_absolute_cinema():
    client = obs_manager.get_client()

    # Guardamos scene actual para volver a ella
    current_scene = client.get_current_program_scene().scene_name ## Guardamos estado inicial

    client.set_current_scene_transition_duration(FADE_IN_MS)

    client.set_current_program_scene(CINEMA_SCENE)

    client.set_current_scene_transition_duration(FADE_OUT_MS)

    time.sleep(0.05)

    client.set_current_program_scene(current_scene)

    client.set_current_scene_transition_duration(DEFAULT_TRANSITION_DURATION)

    ## NO ACCESS TO VERTICAL
    

    # id = client.create_scene_item(scene_name=current_scene, source_name=CINEMA_SCENE, enabled=True).scene_item_id


    # time.sleep(FADE_OUT_MS/1000.0)
    # # Configuracion
    # client.set_scene_item_enabled(
    #     scene_name=current_scene,
    #     item_id=id,
    #     enabled=False
    # )

    # time.sleep(0.05)

    # client.remove_scene_item(
    #     scene_name=current_scene,
    #     item_id=id
    # )

    # Disconnect
    obs_manager.disconnect()


if __name__ == "__main__":
    run_absolute_cinema()