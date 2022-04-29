"""Utility function for generation the user profile."""

# Future Implementations
from __future__ import annotations

# Thirdparty Library
from selenium.webdriver.remote.webelement import WebElement

# Package Library
from SeleniumScraping.base import TorBrowser


def expand_se(
    driver: TorBrowser, element_node: WebElement
) -> list[WebElement]:
    """Expand shadow root element and make 'hidden' nodes accessible.

    Parameters
    ----------
    driver : TorBrowser
        Webdriver initiated by `TorBrowser`.
    element_node : WebElement
        Element containing the shadow root node.

    Returns
    -------
    WebElement.
    """
    shadow_root: list[WebElement] = driver.execute_script(
        "return arguments[0].shadowRoot.children", element_node
    )

    return shadow_root
