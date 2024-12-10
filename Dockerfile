# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

ARG VITE_BACKEND_HOST=127.0.0.1
ARG VITE_BACKEND_PORT=8000
ARG MODEL_PATH

# Build frontend
FROM node:20.4.0 AS build-frontend
WORKDIR /app
COPY ./demo/ ./demo
ENV VITE_BACKEND_HOST=$VITE_BACKEND_HOST
ENV VITE_BACKEND_PORT=$VITE_BACKEND_PORT
ENV VITE_FRONTEND_PATH=/app/demo/dist
WORKDIR /app/demo
RUN npm install && npm run build

# Build backend
FROM python:3.12.0-slim-bookworm
WORKDIR /app

RUN apt-get update && \
    apt-get install --yes --no-install-recommends git=1:2.34.1-1 build-essential=12.9 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-frontend /app/demo/dist ./demo/dist
COPY ./capella_context_diagrams_demonstrator ./capella_context_diagrams_demonstrator
COPY ./pyproject.toml ./
COPY .git .git
RUN pip install --no-cache-dir .

ENV VITE_BACKEND_HOST=$VITE_BACKEND_HOST
ENV VITE_BACKEND_PORT=$VITE_BACKEND_PORT

EXPOSE ${VITE_BACKEND_PORT}

USER nobody

CMD ["capella-context-diagrams-demonstrator", "${MODEL_PATH}"]
