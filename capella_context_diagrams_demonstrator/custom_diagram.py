# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""YAML wrapper for custom diagram collection."""

from __future__ import annotations

import collections.abc as cabc
import typing as t
from dataclasses import dataclass

import capellambse.model as m

Targets: t.TypeAlias = (
    cabc.MutableMapping[str, t.Any]
    | cabc.Sequence[cabc.MutableMapping[str, t.Any]]
)


@dataclass
class CollectorState:
    """State of the collector."""

    repeat_instructions: cabc.MutableMapping[str, t.Any]
    repeat_depth: int
    visited: set[str]


def _perform_instructions(
    state: CollectorState,
    obj: m.ModelElement,
    instructions: cabc.MutableMapping[str, t.Any],
) -> cabc.Iterator[m.ModelElement]:
    if max_depth := instructions.pop("repeat", None):
        state.repeat_instructions = instructions
        state.repeat_depth = max_depth
    if get_targets := instructions.get("get"):
        yield from _perform_get_or_include(
            state, obj, get_targets, create=False
        )
    if include_targets := instructions.get("include"):
        yield from _perform_get_or_include(
            state, obj, include_targets, create=True
        )
    if not get_targets and not include_targets and state.repeat_depth != 0:
        state.repeat_depth -= 1
        yield from _perform_instructions(state, obj, state.repeat_instructions)


def _perform_get_or_include(
    state: CollectorState,
    obj: m.ModelElement,
    targets: Targets,
    *,
    create: bool,
) -> cabc.Iterator[m.ModelElement]:
    if isinstance(targets, cabc.Mapping):
        targets = [targets]
    assert isinstance(targets, cabc.MutableSequence)
    if state.repeat_depth > 0:
        state.repeat_depth += len(targets)
    for i in targets:
        attr = i["name"]
        target = getattr(obj, attr, None)
        if isinstance(target, cabc.Iterator):
            filters = i.get("filter", {})
            for item in target:
                if item.uuid in state.visited:
                    continue
                state.visited.add(item.uuid)
                if any(
                    getattr(obj, key) != value
                    for key, value in filters.items()
                ):
                    continue
                if create:
                    yield item
                yield from _perform_instructions(state, item, i)
        elif isinstance(target, m.ModelElement):
            if target.uuid in state.visited:
                continue
            state.visited.add(target.uuid)
            if create:
                yield target
            yield from _perform_instructions(state, target, i)


def collect(
    target: m.ModelElement, instructions: cabc.MutableMapping[str, t.Any]
) -> cabc.Iterator[m.ModelElement]:
    """Collect the context for a custom diagram."""
    state = CollectorState(
        repeat_instructions={}, repeat_depth=0, visited=set()
    )
    yield from _perform_instructions(state, target, instructions)
