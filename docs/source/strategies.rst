.. currentmodule:: pydantic_forms


Strategies
==================

Pydantic-forms uses the strategy pattern to provide for someof the custom logic you may need when dealing with various
web frameworks.

All strategies inherit from the BaseStrategy class listed below.

The default strategy that is used is a compatible FastAPI/Starlette strategy.

.. autoclass:: BaseStrategy
    :members:





