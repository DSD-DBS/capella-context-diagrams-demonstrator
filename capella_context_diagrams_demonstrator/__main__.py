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
import uvicorn
import yaml
from capellambse.metamodel import cs, fa, information, la, oa, pa, sa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import capella_context_diagrams_demonstrator

from . import custom_diagram, data_model, helpers

PORT = int(os.getenv("CCDD_PORT") or 8000)
HOST = os.environ.get("CCDD_HOST", "127.0.0.1")
PATH_TO_FRONTEND = pathlib.Path(
    os.environ.get("CCDD_FRONTEND_PATH", "./demo/dist")
)
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.model = None
app.state.obj = None
app.state.elements = []


def collect_all_elements() -> list[dict[str, str]]:
    """Collect all elements in the model."""

    def iter_children(parent: m.ModelElement) -> t.Iterator[m.ModelElement]:
        for attr in dir(parent):
            if attr.startswith("_"):
                continue
            acc = getattr(type(parent), attr, None)
            if (
                isinstance(acc, m.DirectProxyAccessor) and not acc.rootelem
            ) or isinstance(acc, m.RoleTagAccessor):
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

    return app.state.elements


def load_model(model: capellambse.MelodyModel) -> None:
    """Load the model."""
    app.state.model = model
    try:
        collect_all_elements()
    except Exception as e:
        raise ValueError(f"Error collecting elements: {e}") from e


app.mount(
    "/assets",
    StaticFiles(directory=PATH_TO_FRONTEND / "assets"),
    name="assets",
)


@app.get("/", status_code=200)
async def root() -> HTMLResponse:
    """Serve the frontend static files."""
    return HTMLResponse(
        content=(PATH_TO_FRONTEND / "index.html").read_text(), status_code=200
    )


@app.get("/api/elements")
async def get_all_elements() -> JSONResponse:
    """Get all elements in the model."""
    return JSONResponse(
        content={
            "status": "success",
            "elements": app.state.elements,
        },
        status_code=200,
    )


@app.post("/api/target")
async def set_target(request: data_model.SetTargetRequest) -> JSONResponse:
    """Set the target object."""
    try:
        app.state.obj = app.state.model.by_uuid(request.uuid)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500,
        )
    return JSONResponse(content={"status": "success"}, status_code=200)


@app.post("/api/render")
async def render_diagram(
    request: data_model.RenderDiagramRequest,
) -> JSONResponse:
    """Render a diagram from a given yaml string."""
    if app.state.obj is None:
        return helpers.make_error_json_response("No target selected", 500)

    try:
        data = yaml.safe_load(request.yaml)
    except yaml.YAMLError as e:
        return helpers.make_error_json_response(str(e), 400)

    if not isinstance(data, dict):
        if not isinstance(data, str):
            return helpers.make_error_json_response("Invalid yaml", 400)
        data = {data: {}}

    if len(data) != 1:
        return helpers.make_error_json_response(
            "Only one diagram can be rendered at a time", 400
        )

    diag_type, attrs = next(iter(data.items()), ("", {}))
    try:
        diag = getattr(app.state.obj, diag_type)
        assert isinstance(attrs, dict)
        if diag_type == "custom_diagram":
            instructions = attrs.pop("collect", {})
            content = diag.render(
                "svg",
                collect=custom_diagram.CustomCollectorWrapper(
                    app.state.obj, instructions
                )(),
                **attrs,
            )
        else:
            content = diag.render("svg", **attrs)
        return helpers.make_json_response(
            "success", diag.name, helpers.modify_svg(content), 200
        )
    except Exception as e:
        return helpers.make_error_json_response(str(e), 500)


@app.get("/api/attributes/")
async def get_attributes(uuid: str) -> JSONResponse:
    """Get the attributes of the selected object."""
    if app.state.model is None:
        return JSONResponse(
            content={"status": "error", "message": "No model loaded"},
            status_code=500,
        )
    obj = app.state.model.by_uuid(uuid)
    return JSONResponse(
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
