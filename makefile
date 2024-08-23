APP_NAME=study_buddy

run-local:
	python -m $(APP_NAME)

PHONY: build publish

build:
	docker build --platform linux/amd64 -t docker.yesidlopez.de/$(APP_NAME):$(VERSION) .

publish: build
publish:
	docker push docker.yesidlopez.de/$(APP_NAME):$(VERSION)

PHONY: update-image-version release publish-with-chart

update-image-version:
	sed -i '' 's/tag: ".*"/tag: "$(VERSION)"/' ./chart/values.yaml

publish-with-chart: publish update-image-version

# Trulens

build-trulens:
	docker build --platform linux/amd64 -t docker.yesidlopez.de/trulens-dashboard:latest trulens_dashboard

publish-trulens: build-trulens
publish-trulens:
	docker push docker.yesidlopez.de/trulens-dashboard:latest

deploy-trulens:
	kubectl apply -f trulens_dashboard/k8s/deployment.yaml
	kubectl apply -f trulens_dashboard/k8s/service.yaml

# Local
deps:
	poetry install

.PHONY: clean-pycache
clean-pycache: ## Clean up pycache files
	find . -name '.mypy_cache' -exec rm -rf {} +
	find . -name '.ruff_cache' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
