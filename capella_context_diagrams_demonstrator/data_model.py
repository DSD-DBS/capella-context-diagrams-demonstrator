# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Data models for Capella Context Diagram Demonstrator."""

import pydantic


class ValidateTargetRequest(pydantic.BaseModel):
    """Request for validating the target object."""

    uuid: str


class RenderDiagramRequest(pydantic.BaseModel):
    """Request for rendering a diagram from a given yaml string."""

    yaml: str
    uuid: str
