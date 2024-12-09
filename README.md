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

# Installation

You can install the latest released version directly from PyPI.

```sh
pip install capella-context-diagrams-demonstrator
```

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

# Development

First run the following commands to create the static files for the backend:

```sh
cd demo
npm install
export VITE_BACKEND_HOST=127.0.0.1
export VITE_BACKEND_PORT=8000
npm run build
```

To develop the frontend, use the following command:

```sh
npm run dev
```

Then run the following command in the root folder to start the backend server:

```sh
capella-context-diagrams-demonstrator {path_to_model}
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
