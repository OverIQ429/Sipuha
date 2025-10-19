import os
import pyara
import asyncio
import concurrent.futures
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from core.database import create_tables

create_tables()

app = FastAPI(
    title="Audio Processing API",
    max_upload_size=10 * 1024 * 1024,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

thread_pool = concurrent.futures.ThreadPoolExecutor(
    max_workers=20,
    thread_name_prefix="audio_worker"
)


@app.get("/")
async def show_window(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    import uuid
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        file_path = Path(tmp_file.name)

    try:
        content = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        try:
            decision = await asyncio.wait_for(
                asyncio.to_thread(pyara.main.predict_audio, str(file_path)),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            return JSONResponse({
                "status": "error",
                "message": "Таймаут обработки"
            }, status_code=408)

        if decision == 1:
            result = "Сгенерированно нейросетью"
        else:
            result = "Звуковая дорожка оригинальна"

        return JSONResponse({
            "status": "success",
            "result": result,
            "message": "Файл успешно обработан"
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"Ошибка: {str(e)}"
        }, status_code=500)

    finally:
        try:
            if file_path.exists():
                os.unlink(file_path)
        except:
            pass


@app.get("/check_sound", response_class=HTMLResponse)
async def check_sound(request: Request, result: str = None):
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "result": result
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)