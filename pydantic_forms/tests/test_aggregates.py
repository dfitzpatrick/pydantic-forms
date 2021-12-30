import pytest

from pydantic_forms.forms import PydanticForm
from pydantic_forms.objects import CsrfError
from pydantic_forms.tests.conftest import MockAsyncRequestForm, MockPostBackRequestForm, SampleFlatSchema


@pytest.mark.asyncio
async def test_response_csrf_checks():
    req = MockAsyncRequestForm()
    form = await PydanticForm.create(req, SampleFlatSchema)
    # Simulate postback
    req.other_fields['csrf'] = form.csrf
    print('test')
    print(await req.form())
    new_form = await PydanticForm.validate_request(req, SampleFlatSchema)
    assert new_form.csrf == req.session['csrf']

@pytest.mark.asyncio
async def test_form_data_shows_form_not_valid():
    request = MockPostBackRequestForm(error=True)
    form_data = await PydanticForm.validate_request(request, SampleFlatSchema)
    assert form_data.is_valid is False

@pytest.mark.asyncio
async def test_form_data_shows_form_valid():
    request = MockPostBackRequestForm(error=False)
    form_data = await PydanticForm.validate_request(request, SampleFlatSchema)
    assert form_data.is_valid is True

@pytest.mark.asyncio
async def test_model_is_correct_type():
    request = MockPostBackRequestForm(error=False)
    form_data = await PydanticForm.validate_request(request, SampleFlatSchema)
    assert isinstance(form_data.model, SampleFlatSchema)

@pytest.mark.asyncio
async def test_csrf_gets_stored_in_session(req):
    form = await PydanticForm.create(req, SampleFlatSchema)
    assert req.session['csrf'] != ''

@pytest.mark.asyncio
async def test_csrf_fails_throws_error():
    request = MockPostBackRequestForm()
    request.session['csrf'] = 'nottherightvalue'
    with pytest.raises(CsrfError):
        foo = await PydanticForm.validate_request(request, SampleFlatSchema)

@pytest.mark.asyncio
async def test_valid_csrf_passes():
    request = MockPostBackRequestForm()
    foo = await PydanticForm.validate_request(request, SampleFlatSchema)
    assert foo is not None

@pytest.mark.asyncio
async def test_invalid_form_has_field_errors():
    request = MockPostBackRequestForm(error=True)
    data = await PydanticForm.validate_request(request, SampleFlatSchema)

@pytest.mark.asyncio
async def test_form_shows_validated_when_validating_request():
    request = MockPostBackRequestForm()
    form = await PydanticForm.validate_request(request, SampleFlatSchema)
    assert form.validated is True

@pytest.mark.asyncio
async def test_form_shows_validated_when_validating_request_and_it_fails():
    request = MockPostBackRequestForm(error=True)
    form = await PydanticForm.validate_request(request, SampleFlatSchema)
    assert form.validated is True


@pytest.mark.asyncio
async def test_form_show_not_validated_when_creating():
    request = MockAsyncRequestForm()
    form = await PydanticForm.create(request, SampleFlatSchema)
    assert form.validated is False

