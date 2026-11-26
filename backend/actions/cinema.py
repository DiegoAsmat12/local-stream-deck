
## BOILERPLATE PORQUE NO SE PYTHON
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time # STAP antes de borrar algo
from obs_client_manager import obs_manager


CINEMA_SCENE = "FX_CINEMA"
CINEMA_IMAGE = "CINEMA_SOURCE"
FILTER_NAME = "FADE_OPACITY"


FADE_IN_MS = 350
FADE_OUT_MS = 3141 # PI?!?!

FADE_FPS = 40 # 40FPS

DEFAULT_TRANSITION_DURATION = 300

# Duration in MS
def _fade_opacity(client ,source_name, start:float , end, duration): 
    steps = max(1, round((duration / 1000.0) *  FADE_FPS))

    delay = 1.0/ FADE_FPS
    

    for i in range(steps+1):
        opacity = start + (end - start) * (i/steps)

        client.set_source_filter_settings(
            source_name=CINEMA_IMAGE,
            filter_name=FILTER_NAME,
            settings={
                "opacity": opacity
            },
            overlay=True
        )

        if i < steps:
            time.sleep(delay)


def run_absolute_cinema():
    client = obs_manager.get_client()

    # Guardamos scene actual para volver a ella
    current_scene = client.get_current_program_scene().scene_name ## Guardamos estado inicial

    # client.set_current_scene_transition_duration(FADE_IN_MS)

    # client.set_current_program_scene(CINEMA_SCENE)

    # client.set_current_scene_transition_duration(FADE_OUT_MS)

    # time.sleep(0.05)

    # client.set_current_program_scene(current_scene)

    # client.set_current_scene_transition_duration(DEFAULT_TRANSITION_DURATION)

    ## NO ACCESS TO VERTICAL
    

    id = client.create_scene_item(scene_name=current_scene, source_name=CINEMA_SCENE, enabled=True).scene_item_id


    _fade_opacity(client, CINEMA_IMAGE, 0.0, 1.0, FADE_IN_MS)


    _fade_opacity(client, CINEMA_IMAGE, 1.0, 0.0, FADE_OUT_MS)


    time.sleep(0.05)

    client.remove_scene_item(scene_name=current_scene, item_id=id)

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