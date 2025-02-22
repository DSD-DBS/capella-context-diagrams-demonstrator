<!--
 ~ Copyright DB InfraGO AG and contributors
 ~ SPDX-License-Identifier: Apache-2.0
 -->

# capella-context-diagrams-demonstrator

![image](https://github.com/DSD-DBS/capella-context-diagrams-demonstrator/actions/workflows/build-test-publish.yml/badge.svg)
![image](https://github.com/DSD-DBS/capella-context-diagrams-demonstrator/actions/workflows/lint.yml/badge.svg)

Demonstrator for Capella Context Diagrams

# Documentation

Read the [full documentation on Github pages](https://dsd-dbs.github.io/capella-context-diagrams-demonstrator).

# Quickstart

Build and run locally with Docker:

```sh
make build
make run MODEL_PATH={path_to_model}
```

The Capella Context Diagrams Demonstrator will be running at `http://localhost:8000`.

# Development

To set up a development environment, clone the project and install it into a
virtual environment.

```sh
git clone https://github.com/DSD-DBS/capella-context-diagrams-demonstrator
cd capella-context-diagrams-demonstrator
python -m venv .venv

source .venv/bin/activate.sh  # for Linux / Mac
.venv\Scripts\activate  # for Windows

pip install -U pip pre-commit
pip install -e '.[docs,test]'
pre-commit install
```

Then run the following commands:

```sh
make build-dev
make run-backend-dev MODEL_PATH={path_to_model}
```

and in a separate terminal:

```sh

make run-frontend-dev
```

The backend server and static frontend will be running at `http://localhost:8000` and the live frontend will be served at `http://localhost:5173`.

# Contributing

We'd love to see your bug reports and improvement suggestions! Please take a
look at our [guidelines for contributors](CONTRIBUTING.md) for details.

# Licenses

This project is compliant with the
[REUSE Specification Version 3.0](https://git.fsfe.org/reuse/docs/src/commit/d173a27231a36e1a2a3af07421f5e557ae0fec46/spec.md).

Copyright DB InfraGO AG, licensed under Apache 2.0 (see full text in
[LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt))

Dot-files are licensed under CC0-1.0 (see full text in
[LICENSES/CC0-1.0.txt](LICENSES/CC0-1.0.txt))
