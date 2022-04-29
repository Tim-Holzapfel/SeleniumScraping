from __future__ import annotations

# Standard Library
from typing import Union, cast, overload


class StrDesc:
    """Descriptor for string variables."""

    def __init__(self, instance_name: str):
        self.str_desc: Union[str, None] = None
        self.instance_name: str = instance_name

    @overload
    def __get__(self, str_desc: None, str_type: None) -> StrDesc:
        ...

    @overload
    def __get__(self, str_desc: object, str_type: type[object]) -> str:
        ...

    def __get__(
        self,
        str_desc: Union[object, None],
        str_type: Union[type[object], None] = None,
    ) -> Union[StrDesc, str]:
        """Get variable value."""
        return cast(str, self.str_desc)

    def __set__(self, str_desc: object, value: str):
        """Set variable."""
        if value is None or self.str_desc == value:
            return
        assert isinstance(value, str)
        # reveal_type(self.str_desc)
        self.str_desc = value

    def __delete__(self, str_desc) -> None:
        del self.str_desc
