# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Main entry point into capella_context_diagrams_demonstrator."""

import click

import capella_context_diagrams_demonstrator


@click.command()
@click.version_option(
    version=capella_context_diagrams_demonstrator.__version__,
    prog_name="capella-context-diagrams-demonstrator",
    message="%(prog)s %(version)s",
)
def main() -> None:
    """Console script for capella_context_diagrams_demonstrator."""


if __name__ == "__main__":
    main()
