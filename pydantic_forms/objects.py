from typing import Any, Optional, Sequence

from pydantic import BaseModel


class FormField(BaseModel):
    """
    A Pydantic model that is created when using :class:`PydanticForm`

    Parameters
    ----------
    name:
        The name of the field from the HTML output. Corresponds to the field of the pydantic model.

    error:
        The error string if applicable after validation.
        For convenience, this is set as an empty string to make it easily injectable into HTML forms.

    value:
        The value of the form field that the user submitted.
        This should not be used to access validated data. Use :attr:`.PydanticForm.model` for that.

        This is helpful to auto-populate forms with data the user entered after a server-side validation.

    """
    name: str
    error: str = ''
    value: Optional[Any] = None

    class Config:
        frozen = True


class ValidationErrorSchema(BaseModel):
    loc: Sequence[str]
    msg: str
    type: str


class CsrfError(Exception):
    pass
