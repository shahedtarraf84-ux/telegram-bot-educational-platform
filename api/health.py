from typing import Dict

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}
