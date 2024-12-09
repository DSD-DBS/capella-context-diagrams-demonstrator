# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""YAML wrapper for custom diagram collection."""

from __future__ import annotations

import collections.abc as cabc
import typing as t

import capellambse.model as m


class CustomCollectorWrapper:
    """Collect the context for a custom diagram."""

    def __init__(
        self,
        target: m.ModelElement,
        instructions: dict[str, t.Any],
    ) -> None:
        self.target: m.ModelElement = target
        self.instructions: dict[str, t.Any] = instructions
        self.repeat_instructions: dict[str, t.Any] = {}
        self.repeat_depth: int = 0
        self.visited: set[str] = set()

    def __call__(self) -> cabc.Iterable[m.ModelElement]:
        yield from self._perform_instructions(self.target, self.instructions)

    def _matches_filters(
        self, obj: m.ModelElement, filters: dict[str, t.Any]
    ) -> bool:
        for key, value in filters.items():
            if getattr(obj, key) != value:
                return False
        return True

    def _perform_instructions(
        self, obj: m.ModelElement, instructions: dict[str, t.Any]
    ) -> cabc.Iterable[m.ModelElement]:
        if max_depth := instructions.pop("repeat", None):
            self.repeat_instructions = instructions
            self.repeat_depth = max_depth
        if get_targets := instructions.get("get"):
            yield from self._perform_get_or_include(
                obj, get_targets, create=False
            )
        if include_targets := instructions.get("include"):
            yield from self._perform_get_or_include(
                obj, include_targets, create=True
            )
        if not get_targets and not include_targets and self.repeat_depth != 0:
            self.repeat_depth -= 1
            yield from self._perform_instructions(
                obj, self.repeat_instructions
            )

    def _perform_get_or_include(
        self,
        obj: m.ModelElement,
        targets: dict[str, t.Any] | list[dict[str, t.Any]],
        *,
        create: bool,
    ) -> cabc.Iterable[m.ModelElement]:
        if isinstance(targets, dict):
            targets = [targets]
        assert isinstance(targets, list)
        if self.repeat_depth > 0:
            self.repeat_depth += len(targets)
        for i in targets:
            attr = i.get("name")
            assert attr, "Attribute name is required."
            target = getattr(obj, attr, None)
            if isinstance(target, cabc.Iterable):
                filters = i.get("filter", {})
                for item in target:
                    if item.uuid in self.visited:
                        continue
                    self.visited.add(item.uuid)
                    if not self._matches_filters(item, filters):
                        continue
                    if create:
                        yield item
                    yield from self._perform_instructions(item, i)
            elif isinstance(target, m.ModelElement):
                if target.uuid in self.visited:
                    continue
                self.visited.add(target.uuid)
                if create:
                    yield target
                yield from self._perform_instructions(target, i)
                yield from self._perform_instructions(target, i)
