from fastapi import FastAPI
from routes import router

app = FastAPI()

router.include_router(router)
