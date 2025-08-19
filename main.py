from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
import pyara
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def show_window(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    # allowed_extensions = {'.wav', '.mp3', '.ogg', '.flac'}
    file_path = UPLOAD_DIR / file.filename
    # file_extension = file_path.suffix.lower()
    #
    # if file_extension not in allowed_extensions:
    #     return JSONResponse({
    #         "status": "error",
    #         "message": f"Неподдерживаемый формат. Используйте: {', '.join(allowed_extensions)}"
    #     }, status_code=400)
    #
    # max_size = 10 * 1024 * 1024
    # content = await file.read()
    # if len(content) > max_size:
    #     return JSONResponse({
    #         "status": "error",
    #         "message": "Файл слишком большой (макс. 10MB)"
    #     }, status_code=400)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    decision = pyara.main.predict_audio(file_path)
    if decision == 1:
        result = "Сгенерированно нейросетью"
    else:
        result = "Звуковая дорожка оригинальна"
    os.unlink(file_path)
    return JSONResponse({
        "status": "success",
        "result": result,
        "message": "Файл успешно обработан"
    })

@app.get("/check_sound", response_class=HTMLResponse)
async def check_sound(request: Request, result: str = None):
    print(f"Передано в шаблон: result={result}, тип={type(result)}")
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