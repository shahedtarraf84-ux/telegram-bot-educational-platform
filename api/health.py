from typing import Dict

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def health() -> Dict[str, str]:
    return {"status": "ok"}
