# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Main entry point into capella_context_diagrams_demonstrator."""

from __future__ import annotations

import os
import pathlib
import typing as t

import capellambse
import capellambse.model as m
import click
import fastapi
import uvicorn
import yaml
from capellambse.metamodel import cs, fa, information, la, oa, pa, sa
from fastapi import responses, staticfiles
from fastapi.middleware import cors

import capella_context_diagrams_demonstrator

from . import custom_diagram, data_model, helpers

PORT = int(os.getenv("VITE_CCDD_BACKEND_PORT") or 8000)
HOST = os.environ.get("VITE_CCDD_BACKEND_HOST", "127.0.0.1")
PATH_TO_FRONTEND = pathlib.Path(os.getenv("VITE_FRONTEND_PATH", "./demo/dist"))
ELEMENT_TYPES = frozenset(
    {
        oa.Entity,
        oa.OperationalActivity,
        oa.OperationalCapability,
        oa.CommunicationMean,
        sa.Mission,
        sa.Capability,
        sa.SystemComponent,
        sa.SystemFunction,
        la.LogicalComponent,
        la.LogicalFunction,
        pa.PhysicalComponent,
        pa.PhysicalFunction,
        cs.PhysicalLink,
        cs.PhysicalPort,
        fa.ComponentExchange,
        information.Class,
    }
)

app = fastapi.FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.model = None
app.state.elements = []


def collect_all_elements() -> None:
    """Collect all elements in the model."""

    def iter_children(parent: m.ModelElement) -> t.Iterator[m.ModelElement]:
        for attr in dir(parent):
            if attr.startswith("_"):
                continue
            acc = getattr(type(parent), attr, None)
            if (
                isinstance(acc, m.DirectProxyAccessor) and not acc.rootelem
            ) or isinstance(acc, m.Containment):
                if acc.aslist is None:
                    if (child := getattr(parent, attr)) is not None:
                        yield child
                else:
                    yield from getattr(parent, attr)

    def get_children_recursive(
        parent: m.ModelElement,
    ) -> t.Iterator[m.ModelElement]:
        for child in iter_children(parent):
            yield child
            yield from get_children_recursive(child)

    model = app.state.model
    for layer in (model.pa, model.la, model.sa, model.oa):
        for ele in get_children_recursive(layer):
            if type(ele) in ELEMENT_TYPES:
                app.state.elements.append({"uuid": ele.uuid, "name": ele.name})


def load_model(model: capellambse.MelodyModel) -> None:
    """Load the model."""
    app.state.model = model
    try:
        collect_all_elements()
    except Exception as exc:
        raise ValueError(f"Error collecting elements: {exc}") from exc


app.mount(
    "/examples",
    staticfiles.StaticFiles(directory=PATH_TO_FRONTEND / "examples"),
    name="examples",
)

app.mount(
    "/assets",
    staticfiles.StaticFiles(directory=PATH_TO_FRONTEND / "assets"),
    name="assets",
)


@app.get("/", status_code=200)
async def root() -> responses.HTMLResponse:
    """Serve the frontend static files."""
    return responses.HTMLResponse(
        content=(PATH_TO_FRONTEND / "index.html").read_text(), status_code=200
    )


@app.get("/favicon.ico", status_code=200)
async def favicon() -> responses.HTMLResponse:
    """Serve the favicon."""
    return responses.FileResponse(PATH_TO_FRONTEND / "favicon.ico")


@app.get("/api/elements")
async def get_all_elements() -> responses.JSONResponse:
    """Get all elements in the model."""
    return responses.JSONResponse(
        content={
            "status": "success",
            "elements": app.state.elements,
        },
        status_code=200,
    )


@app.post("/api/validate")
async def validate_target(
    request: data_model.ValidateTargetRequest,
) -> responses.JSONResponse:
    """Validate the target object."""
    try:
        app.state.model.by_uuid(request.uuid)
    except KeyError as error:
        return responses.JSONResponse(
            content={
                "status": "error",
                "message": str(error),
                "name": "UUID not found",
            },
            status_code=400,
        )
    except Exception as exc:
        return responses.JSONResponse(
            content={
                "status": "error",
                "message": str(exc),
                "name": type(exc).__name__,
            },
            status_code=500,
        )
    return responses.JSONResponse(
        content={"status": "success"}, status_code=200
    )


@app.post("/api/render")
async def render_diagram(
    request: data_model.RenderDiagramRequest,
) -> responses.JSONResponse:
    """Render a diagram from a given yaml string and target uuid."""
    try:
        target = app.state.model.by_uuid(request.uuid)
        data = yaml.safe_load(request.yaml)
    except KeyError as error:
        return helpers.make_error_json_response(
            str(error), 400, "UUID not found"
        )
    except Exception as exc:
        return helpers.make_error_json_response(
            str(exc), 400, type(exc).__name__
        )

    if not isinstance(data, dict):
        if not isinstance(data, str):
            return helpers.make_error_json_response(
                "The YAML description must be a string or a dictionary",
                400,
                "Invalid YAML",
            )
        data = {data: {}}

    if len(data) != 1:
        return helpers.make_error_json_response(
            "Only one diagram can be rendered at a time", 400, "Invalid YAML"
        )

    diag_type, attrs = next(iter(data.items()), ("", {}))
    try:
        diag = getattr(target, diag_type)
        assert isinstance(attrs, dict)
        if diag_type == "custom_diagram":
            instructions = attrs.pop("collect", {})
            content = diag.render(
                "svg",
                collect=custom_diagram.collect(target, instructions),
                **attrs,
            )
        else:
            content = diag.render("svg", **attrs)
        return helpers.make_json_response(
            "success", diag.name, helpers.modify_svg(content), 200
        )
    except Exception as exc:
        return helpers.make_error_json_response(
            str(exc), 500, type(exc).__name__
        )


@app.get("/api/attributes/")
async def get_attributes(uuid: str) -> responses.JSONResponse:
    """Get the attributes of the selected object."""
    obj = app.state.model.by_uuid(uuid)
    return responses.JSONResponse(
        content={
            "status": "success",
            "name": obj.name,
            "repr": helpers.modify_h1_tag(obj.__html__()),
        },
        status_code=200,
    )


@click.command()
@click.version_option(
    version=capella_context_diagrams_demonstrator.__version__,
    prog_name="capella-context-diagrams-demonstrator",
    message="%(prog)s %(version)s",
)
@click.argument("model", type=capellambse.ModelCLI())
def startup(model: capellambse.MelodyModel) -> None:
    """Start the FastAPI server."""
    load_model(model)
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    startup()
