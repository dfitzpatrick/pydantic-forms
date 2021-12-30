import asyncio
from typing import Dict, Any

import pytest
from pydantic import BaseModel

from pydantic_forms import DefaultStrategy

class SampleFlatSchema(BaseModel):
    foo: int
    bar: bool

class MockAsyncRequestForm:


    def __init__(self, error=False):
        self.model = SampleFlatSchema(foo=1, bar=True)
        self.error = error
        self.session = {}
        self.other_fields = {}

    async def form(self) -> Dict[str, Any]:
        if self.error:
            return self.other_fields
        result = {**self.other_fields, **self.model.dict()}
        return result

    def __repr__(self):
        data = asyncio.run(self.form())
        return f"MockAsyncRequestForm(form()={data}, other_fields={self.other_fields}, error={self.error}, session={self.session})"


class MockPostBackRequestForm(MockAsyncRequestForm):
    model = SampleFlatSchema(foo=1, bar=True)
    def __init__(self, error=False):
        super(MockPostBackRequestForm, self).__init__(error)
        self.other_fields = {}
        self.other_fields['csrf'] = 'testcsrfvalid'
        self.session['csrf'] = self.other_fields['csrf']


@pytest.fixture
def req():
    yield MockAsyncRequestForm()

@pytest.fixture
def strategy():
    yield DefaultStrategy()


class SampleFlatSchema(BaseModel):
    foo: int
    bar: bool