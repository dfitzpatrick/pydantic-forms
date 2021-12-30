
About
===========
Pydantic Forms takes a very simplistic approach to form validation.
Create a Pydantic Model to represent your form data, and utilize Pydantic's own
strong validation logic at your disposal.

Some libraries require you to define custom classes for forms and work to auto-generate HTML
for you. This library is NOT one of those.

* Pydantic Models are just Plain Old Pydantic Models. No extra logic
  from this library needs to be injected into it. Use your existing models.

* HTML generation is up to the user. Create your templates as simple or
  as complex as you would like. Utilize macros for complex error display.

**Full Documentation: `ReadTheDocs <https://pydantic-forms.readthedocs.io/en/latest/>`_


Examples
===========
FastAPI example

.. code-block:: python3

   from fastapi import FastAPI
   from fastapi.requests import Request
   from fastapi.responses import HTMLResponse
   from fastapi.templating import Jinja2Templates
   from pydantic import BaseModel, validator, constr, ValidationError
   from pydantic_forms import PydanticForm

   # Needed to access FastAPI Request Session data
   from starsessions import SessionMiddleware



   templates = Jinja2Templates(directory="templates")
   app = FastAPI()
   app.add_middleware(SessionMiddleware, secret_key="secret", autoload=True)

   class MyForm(BaseModel):
       name: constr(min_length=1)  # Supported Pydantic constrained types
       age: int

       # pydantic validators work too
       @validator('age')
       def age_must_be_over_30(cls, value, values):
           if value <= 30:
               raise ValueError("30's are your new 20's")
           return value

   @app.get('/myform', response_class=HTMLResponse)
   async def get_my_form(request: Request):
       form = await PydanticForm.create(request, MyForm)
       return templates.TemplateResponse("myform.html", {"request": request, 'form': form})

   @app.post('/myform', response_class=HTMLResponse)
   async def handle_my_form(request: Request):
       form = await PydanticForm.validate_request(request, MyForm)
       if form.is_valid:
           model = form.model
           return f"Hello {model.name} you are {model.age} years old"
       else:
           return templates.TemplateResponse("myform.html", {"request": request, 'form': form})


*Using Jinja2 (myform.html)*

.. code-block:: html

   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>My Form</title>
   </head>
   <body>
       <form method="POST">
           <input type="hidden" name="csrf" value="{{form.csrf}}" />


           <label for="name">Name</label>
           <input type="text" name="name" id="name" value="{{form.fields.name.value}}" />
           <div>{{form.fields.name.error}}</div>

            <label for="age">Age</label>
           <input type="text" name="age" id="age" value="{{form.fields.age.value}}" />
           <div>{{form.fields.age.error}}</div>
           <input type="submit" />
       </form>
   </body>
   </html>

For complex forms that require a lot of validation, utilize **Macros** in
your template library.

Installing
===========
Install Pydantic Forms using poetry
`from Github <https://github.com/dfitzpatrick/pydantic-forms.git>`_

.. note::

   The Default Strategy described in the table of contents uses the request
   session for validation. FastAPI requires `starsessions` to be installed
   for this to work
