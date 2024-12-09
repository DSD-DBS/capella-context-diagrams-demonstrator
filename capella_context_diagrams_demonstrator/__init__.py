# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""The capella_context_diagrams_demonstrator package."""

from importlib import metadata

try:
    __version__ = metadata.version("capella_context_diagrams_demonstrator")
except metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"
del metadata
