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

    state.repeat_depth += len(targets) if state.repeat_depth > 0 else 0

    for instruction in targets:
        yield from _process_target(
            state, obj, instruction["name"], instruction, create=create
        )


def _filter_and_yield(
    state: CollectorState,
    obj: m.ModelElement,
    filters: dict[str, t.Any],
    instructions: dict[str, t.Any],
    *,
    create: bool,
) -> cabc.Iterator[m.ModelElement]:
    if obj.uuid in state.visited:
        return
    state.visited.add(obj.uuid)

    if any(getattr(obj, key) != value for key, value in filters.items()):
        return

    if create:
        yield obj

    yield from _perform_instructions(state, obj, instructions)


def _process_target(
    state: CollectorState,
    obj: m.ModelElement,
    attr: str,
    instructions: dict[str, t.Any],
    *,
    create: bool,
) -> cabc.Iterator[m.ModelElement]:
    target = getattr(obj, attr, None)
    if isinstance(target, cabc.Iterable) and not isinstance(target, str):
        filters = instructions.get("filter", {})
        for item in target:
            yield from _filter_and_yield(
                state, item, filters, instructions, create=create
            )
    elif isinstance(target, m.ModelElement):
        yield from _filter_and_yield(
            state, target, {}, instructions, create=create
        )


def collector(
    target: m.ModelElement, instructions: cabc.MutableMapping[str, t.Any]
) -> cabc.Iterator[m.ModelElement]:
    """Collect model elements based on the provided instructions.

    Parameters
    ----------
    target
        The starting model element to traverse.
    instructions
        A mapping of instructions, for details see:
        https://dsd-dbs.github.io/capella-context-diagrams-demonstrator/

    Yields
    ------
    model_elements
        Model elements that match the given instructions.
    """
    state = CollectorState(
        repeat_instructions={}, repeat_depth=0, visited=set()
    )
    yield from _perform_instructions(state, target, instructions)
