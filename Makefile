.PHONY: build push deploy test clean

IMAGE_NAME=quay.io/karthik099/ai-inference
IMAGE_TAG=latest
NAMESPACE=ai-workload

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

push:
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

deploy:
	oc apply -f k8s/namespace.yaml
	oc apply -f k8s/ -n $(NAMESPACE)

deploy-helm:
	helm upgrade --install ai-inference helm/ai-inference -n $(NAMESPACE) --create-namespace

test:
	pytest app/tests/ -v --cov=app

lint:
	flake8 app/ --count --statistics

rollback:
	ansible-playbook -i ansible/inventory.ini ansible/rollback.yaml

clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	oc delete namespace $(NAMESPACE) || true

local-run:
	docker-compose up -d

local-stop:
	docker-compose down

logs:
	oc logs -f deployment/ai-inference -n $(NAMESPACE)

scale:
	oc scale deployment/ai-inference --replicas=$(REPLICAS) -n $(NAMESPACE)

status:
	oc get all -n $(NAMESPACE)
