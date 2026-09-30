from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain
from learning_path import recommend
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize

app = FastAPI(title="EduGenie")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

TASKS = {
    "qa": ("Q&A", answer_question),
    "explain": ("Explain", explain),
    "quiz": ("Quiz", generate_quiz),
    "summarize": ("Summary", summarize),
    "learn": ("Learning Path", recommend),
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": TASKS,
            "result": None,
            "selected_task": "qa",
            "user_text": "",
            "error": None,
            "label": "",
        },
    )


@app.post("/run", response_class=HTMLResponse)
async def run_task(
    request: Request,
    task: str = Form(...),
    text: str = Form(...),
):
    text = text.strip()

    if task not in TASKS:
        raise HTTPException(
            status_code=400,
            detail="Please select a task.",
        )

    if not text:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "tasks": TASKS,
                "result": None,
                "selected_task": task,
                "user_text": "",
                "error": "Please enter a question or some study text.",
                "label": "",
            },
            status_code=400,
        )

    if len(text) > 12000:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "tasks": TASKS,
                "result": None,
                "selected_task": task,
                "user_text": text,
                "error": "Text must be 12,000 characters or fewer.",
                "label": "",
            },
            status_code=400,
        )

    label, function = TASKS[task]

    try:
        result = function(text)
        error = None
    except (HTTPException, ValueError, RuntimeError) as problem:
        result = None
        error = getattr(problem, "detail", str(problem))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": TASKS,
            "result": result,
            "selected_task": task,
            "user_text": text,
            "error": error,
            "label": label,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
