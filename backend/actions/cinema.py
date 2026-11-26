
## BOILERPLATE PORQUE NO SE PYTHON
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time # STAP antes de borrar algo
from obs_client_manager import obs_manager


from fastapi import APIRouter, BackgroundTasks

router = APIRouter(prefix="/actions", tags=["Actions"])

CINEMA_SCENE = "FX_CINEMA"
CINEMA_IMAGE = "CINEMA_SOURCE"
FILTER_NAME = "FADE_OPACITY"


FADE_IN_MS = 350
FADE_OUT_MS = 3141 # PI?!?!

FADE_FPS = 40 # 40FPS

DEFAULT_TRANSITION_DURATION = 300

# Duration in MS
def _fade_opacity(source_name: str, start:float , end:float, duration: int): 
    steps = max(1, round((duration / 1000.0) *  FADE_FPS))

    delay = 1.0/ FADE_FPS
    

    for i in range(steps+1):
        opacity = start + (end - start) * (i/steps)

        with obs_manager.with_lock() as client:
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

    with obs_manager.with_lock() as client:


        current_scene = client.get_current_program_scene().scene_name

        id = client.create_scene_item(scene_name=current_scene, source_name=CINEMA_SCENE, enabled=True).scene_item_id

    try:

        _fade_opacity(CINEMA_IMAGE, 0.0, 1.0, FADE_IN_MS)


        _fade_opacity(CINEMA_IMAGE, 1.0, 0.0, FADE_OUT_MS)


        

    finally:
        with obs_manager.with_lock() as client:
            time.sleep(0.05)
            client.remove_scene_item(scene_name=current_scene, item_id=id)


@router.post("/cinema")
def trigger_cinema(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_absolute_cinema)
    return {"status": "ok"}


if __name__ == "__main__":
    run_absolute_cinema()