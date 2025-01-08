# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

.PHONY: build-dev run-dev build clean run help

VITE_CCDD_BACKEND_HOST ?= 127.0.0.1
VITE_CCDD_BACKEND_PORT ?= 8000
MODEL_PATH ?=
IMAGE_NAME ?= capella-context-diagrams-demonstrator
VERSION ?= latest

build-dev:
	@echo "Installing dev dependencies..."
	cd demo && npm install && npm run build

run-dev:
	@echo "Starting dev server..."
	cd demo && npm run dev & $(IMAGE_NAME) $(MODEL_PATH)

build:
	@echo "Building $(IMAGE_NAME):$(VERSION) Docker image..."
	docker build \
		--build-arg VITE_CCDD_BACKEND_HOST=$(VITE_CCDD_BACKEND_HOST) \
		--build-arg VITE_CCDD_BACKEND_PORT=$(VITE_CCDD_BACKEND_PORT) \
		-t $(IMAGE_NAME):$(VERSION) .

clean:
	@echo "Cleaning up dangling images..."
	docker container prune -f && docker image prune -f

run:
	@echo "Running $(IMAGE_NAME):$(VERSION) Docker container..."
	docker run -v $(MODEL_PATH):/model -p $(VITE_CCDD_BACKEND_PORT):$(VITE_CCDD_BACKEND_PORT) $(IMAGE_NAME):$(VERSION)

help:
	@echo "Makefile commands:"
	@echo "  build-dev      build development environment"
	@echo "  run-dev          Start the development server"
	@echo "  build        Build the Docker image with specified arguments"
	@echo "  clean        Remove dangling Docker images"
	@echo "  run          Run the Docker container locally"
	@echo "  help         Show this help message"
