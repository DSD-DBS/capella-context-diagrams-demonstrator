# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

.PHONY: build clean run help

FRONTEND_BASE ?= node:20
BACKEND_BASE ?= python:3.12-slim-bookworm
PORT ?= 8000
IMAGE_NAME ?= capella-context-diagrams-demonstrator
VERSION ?= latest

build:
	@echo "Building $(IMAGE_NAME):$(VERSION) Docker image..."
	docker build \
		--build-arg FRONTEND_BASE=$(FRONTEND_BASE) \
		--build-arg BACKEND_BASE=$(BACKEND_BASE) \
		--build-arg PORT=$(PORT) \
		-t $(IMAGE_NAME):$(VERSION) .

clean:
	@echo "Cleaning up dangling images..."
	docker container prune -f && docker image prune -f

run:
	@echo "Running $(IMAGE_NAME):$(VERSION) Docker container..."
	docker run -p $(PORT):$(PORT) $(IMAGE_NAME):$(VERSION)

help:
	@echo "Makefile commands:"
	@echo "  build        Build the Docker image with specified arguments"
	@echo "  clean        Remove dangling Docker images"
	@echo "  run          Run the Docker container locally"
	@echo "  help         Show this help message"
