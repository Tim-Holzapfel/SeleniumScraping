"""Method Exceptions."""

# Future Implementations
from __future__ import annotations

# Standard Library
from inspect import currentframe
from typing import Optional


class DriverBaseException(Exception):
    """Base Class for raising Exceptions."""

    def __init__(
        self,
        message: Optional[str] = None,
        errors: Optional[str] = None,  # pylint: disable=unused-argument
    ):
        """Driver exception class.

        Parameters
        ----------
        message : str, optional
            Additional message to print. The default is None.
        errors : str, optional
            Additional error information. The default is None.

        Returns
        -------
        None.
        """
        c_frame = currentframe()
        assert c_frame is not None
        c_back_frame = c_frame.f_back
        assert c_back_frame is not None
        self.message = message
        self.errors = f"Error occured in {c_back_frame.f_code.co_name}!"

    def __str__(self):
        """Output format when raising the exception with a message."""
        return f"{self.message} {self.errors}"


class InvalidISOError(DriverBaseException):
    """Raise if the specified country does not exist."""

    def __init__(
        self,
        message: Optional[str] = None,
        errors: Optional[str] = None,
    ):
        """Exception for invalid Alpha-3 ISO country codes.

        Parameters
        ----------
        message : str, optional
            Additional message to print. The default is None.
        errors : str, optional
            Additional error information. The default is None.

        Returns
        -------
        None.
        """
        c_frame = currentframe()
        assert c_frame is not None
        c_frame_back = c_frame.f_back
        assert c_frame_back is not None
        self.message = (
            "The specified country does not seem to exist. Maybe a typo?"
        )
        self.errors = f"Error occured in {c_frame_back.f_code.co_name}!"

    def __str__(self):
        """Output format when raising the exception with a message."""
        return f"{self.message} {self.errors}"


class LastPageError(DriverBaseException):
    """Raise if the current page is the last page."""

    ...


class NoFlagFoundError(DriverBaseException):
    """Raise if the country flag could not be selected."""

    ...


class NoSMSCodeError(DriverBaseException):
    """Raise if familysearch.org did not send an account activation code."""

    ...


class NoResultsFoundError(DriverBaseException):
    """Raise if the search query did not produce any results."""

    ...


class DescriptorError(DriverBaseException):
    """Raise if an descriptor is not set properly."""

    ...


class BotCheckInvoked(DriverBaseException):
    """Raise if Familysearch claims that there are no results to show."""


class ProfileError(DriverBaseException):
    """Raise if the current profile is not valid and delete the profile."""

    ...


class TorStartError(DriverBaseException):
    """Raise if Tor could not be started."""

    ...


class WrongPageError(DriverBaseException):
    """Raise if the page context is not correct."""

    ...
