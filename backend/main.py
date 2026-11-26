from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from obs_client_manager import obs_manager
from actions import actions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        obs_manager.connect()
    except Exception as ex:
        print(f"⚠️ OBS not ready on startup (will auto-connect on first action): {ex}")
    yield
    obs_manager.disconnect()


app = FastAPI(title="Local Stream Deck Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(actions_router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)