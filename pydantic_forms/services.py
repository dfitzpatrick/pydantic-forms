from typing import List, Dict, Any, Optional, Type

from pydantic import BaseModel, ValidationError

from .objects import ValidationErrorSchema, FormField


def get_fields(schema: Type[BaseModel]) -> List[str]:
    return list(schema.__fields__.keys())

def format_validation_error_schemas(exception: ValidationError) -> List[ValidationErrorSchema]:
    container = []
    for e in exception.errors():
        container.append(ValidationErrorSchema(
            loc=e['loc'],
            msg=e['msg'],
            type=e['type']
        ))
    return container

def get_field_errors(errors: List[ValidationErrorSchema]) -> Dict[str, str]:
    return {loc: e.msg for e in errors for loc in e.loc}

def make_form_fields(model: Optional[BaseModel], schema: Type[BaseModel], errors: Dict[str, str], data: Optional[Dict[str, Any]] = None) -> Dict[str, FormField]:
    """

    Returns
    -------
    object
    """
    fields = get_fields(schema)
    container = {}

    for field_name in fields:
        value_container = model.dict() if model is not None else data or {}
        value = value_container.get(field_name, '')
        o = FormField(
            name=field_name,
            error=errors.get(field_name, ''),
            value=value
        )
        container[field_name] = o
    return container
