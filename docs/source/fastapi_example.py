
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic_forms import PydanticForm
from pydantic import BaseModel

templates = Jinja2Templates(directory="my/template/directory")
app = FastAPI()

class MyForm(BaseModel):
    name: str
    age: int

@app.get('/my_form', response_class=HTMLResponse)
async def get_my_form(request: Request):
    form = await PydanticForm.create(request, MyForm)
    return templates.TemplateResponse("myform.html", {"request": request, 'form': form})

@app.post('/my_form', response_class=HTMLResponse)
async def handle_my_form(request: Request):
    form = await PydanticForm.validate_request(request, MyForm)
    if form.is_valid:
        model = form.model
        return f"Hello {model.name} you are {model.age} years old"
    else:
        return templates.TemplateResponse("myform.html", {"request": request, 'form': form})

