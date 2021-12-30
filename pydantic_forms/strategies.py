from secrets import token_urlsafe
from typing import Optional, Any, Dict

from .interfaces import BaseStrategy
from .objects import CsrfError


class DefaultStrategy(BaseStrategy):
    csrf_key = 'csrf'

    async def get_request_data(self, request: Any) -> Dict[str, Any]:
        return await request.form()

    async def make_csrf(self) -> str:
        return token_urlsafe(16)

    async def attach_csrf(self, request, csrf) -> Any:
        request.session['csrf'] = csrf
        return request

    async def csrf_check(self, request, csrf_form_data: Optional[str]) -> None:
        session_csrf = request.session.get(self.csrf_key)
        if csrf_form_data is None or session_csrf != csrf_form_data:
            raise CsrfError
