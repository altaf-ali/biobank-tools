"""This file provides a meta class for a singleton object."""

from typing import Any


class Singleton(type):
    """Singleton class.

    A singleton pattern that can be used as a metaclass to ensure only one
    instance of the target class is ever instantiated
    """

    def __init__(self, name, bases, dic):
        self._instance = None
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs) -> Any:
        """Metcalsss __call__ method.

        Overrides the __call__ function so we can eiter return an existing
        instance or create a new one if necessary.

        Args:
            *args: List of positional arguments
            **kwargs: Dictionary of keywork arguments

        Returns:
            An instance of the singleton class
        """
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
