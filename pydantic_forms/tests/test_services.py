from typing import List, Dict, Any

import pydantic
import pytest

from pydantic_forms.strategies import DefaultStrategy
from pydantic_forms.objects import ValidationErrorSchema, FormField
from pydantic import BaseModel
from pydantic_forms.services import *

class SampleSchemaNested(BaseModel):
    foo: int
    bar: int

class SampleSchema(BaseModel):
    standard: str
    a_list: List[SampleSchemaNested]
    a_nested: SampleSchemaNested
    a_dict: Dict[str, SampleSchemaNested]

class SampleFlatSchema(BaseModel):
    foo: int
    bar: bool

@pytest.fixture
def schema():
    yield SampleFlatSchema(foo=1, bar=False)


def test_get_fields(schema):
    ds = DefaultStrategy()
    fields = get_fields(schema)
    assert sorted(fields) == sorted(['foo', 'bar'])

def test_get_field_errors():
    try:
        schema = SampleFlatSchema(foo='foo', bar='bar')
    except pydantic.ValidationError as ve:
        errors = ve.errors()
        errors = [ValidationErrorSchema(**e) for e in errors]
        field_errors = get_field_errors(errors)
        assert field_errors == {'bar': 'value could not be parsed to a boolean', 'foo': 'value is not a valid integer'}

def test_make_form_fields_invalid():
    schema = SampleFlatSchema
    model = None
    data = {'foo': 'foo', 'bar': 'bar'}
    try:
        model = schema(**data)
    except pydantic.ValidationError as ve:
        errors = [ValidationErrorSchema(**e) for e in ve.errors()]
        field_errors = get_field_errors(errors)
        form_fields = make_form_fields(model, schema, field_errors, data)
        assert form_fields == {'bar': FormField(error='value could not be parsed to a boolean', value='bar', name='bar'), 'foo': FormField(error='value is not a valid integer', value='foo', name='foo')}

def test_make_form_fields_valid(schema):
    schema = SampleFlatSchema
    data = {'foo': 1, 'bar': True}
    model = schema(**data)
    field_errors = {}
    form_fields = make_form_fields(model, schema, field_errors)
    assert form_fields == {'bar': FormField(error='', value=True, name='bar'), 'foo': FormField(error='', value=1, name='foo')}

