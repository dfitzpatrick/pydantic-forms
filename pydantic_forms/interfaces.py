from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from typing import TypeVar

Request = TypeVar('Request')

class BaseStrategy(ABC):
    """
    Determines the logic for using request objects and performing csrf operations
    """

    @property
    @abstractmethod
    def csrf_key(self) -> str:
        """
        The csrf key name that will be embedded into HTML forms

        """
        ...

    @abstractmethod
    async def make_csrf(self) -> str:
        """
        Responsible for generating the csrf tokens using a specific algorithm.

        """
        ...

    @abstractmethod
    async def get_request_data(self, request: Request) -> Dict[str, Any]:
        """
        Extracts form data from the request object provided.
        The method transforms the results into a Dictionary where the key is the
        field name and the value is the form data.

        Parameters
        ----------
        request
            The webserver 'request' object that is returned from the user.
        Returns
        -------

        """
        ...

    @abstractmethod
    async def attach_csrf(self, request: Any, csrf: str) -> Any:
        """
        Responsible for attaching the csrf to a medium that the user can later retrieve it from.
        The DefaultStrategy attaches this to the request session.

        Parameters
        ----------
        request
            The webserver 'request' object that is returned from the user.

        csrf
            The generated csrf token
        Returns
        -------
        The modified request object
        """
        ...
    @abstractmethod
    async def csrf_check(self, request, csrf_form_data: Optional[str]) -> None:
        """
        Performs the CSRF check logic.
        An invalid CSRF check will raise CsrfError

        Parameters
        ----------
        request
        csrf_form_data

        Raises
        -------
        CsrfError
            The csrf check was invalid

        Returns
        -------

        """
        ...



