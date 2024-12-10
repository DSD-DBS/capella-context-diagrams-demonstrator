# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Helper functions."""

from __future__ import annotations

import html

import markupsafe
from fastapi import responses
from lxml import etree


def modify_h1_tag(content: str) -> markupsafe.Markup:
    """Modify the h1 tag in the content."""
    parser = etree.HTMLParser()
    tree = etree.fromstring(content, parser)
    for h1 in tree.iter("h1"):
        h1.attrib["style"] = (
            "display: flex; align-items: baseline; gap: 5px; font-size: 120%;"
        )
    return markupsafe.Markup(
        etree.tostring(tree, pretty_print=True, method="html").decode()
    )


def modify_svg(
    svg_content: str,
    new_width: str = "100%",
    new_height: str = "100%",
    new_id: str = "pan-zoom",
) -> markupsafe.Markup:
    """Modify SVG to work with pan-zoom library."""
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(svg_content, parser=parser)

    root.set("width", new_width)
    root.set("height", new_height)
    root.set("id", new_id)

    return markupsafe.Markup(etree.tostring(root).decode())


def _get_error_svg(message: str) -> markupsafe.Markup:
    sanitized_message = html.escape(message)
    return markupsafe.Markup(
        '<svg height="100%" width="100%" id="pan-zoom">'
        '<text x="10" y="40" font-size="24" fill="red">'
        f"{sanitized_message}</text></svg>"
    )


def make_json_response(
    status: str, svg_name: str, content: str, status_code: int
) -> responses.JSONResponse:
    """Create a SVG JSON response."""
    return responses.JSONResponse(
        content={
            "status": status,
            "svg": {
                "name": svg_name,
                "content": content,
            },
        },
        status_code=status_code,
    )


def make_error_json_response(
    message: str, status_code: int
) -> responses.JSONResponse:
    """Create an error JSON response."""
    return make_json_response(
        "error", "error", _get_error_svg(message), status_code
    )
