DOCKER_REGISTRY:=reg.personal.com:8050/fastapi_demo

.PHONY:init
init:
	python -m pip install --upgrade pip
	pip install -r ./requirements.txt

.PHONY:run
run:
	gunicorn main:app -c config/gunicorn_config.py
# sadddsas
.PHONY:build
build\:base:
	pip freeze> requirements.txt
	#sudo docker rmi -f ${DOCKER_REGISTRY}/builder
	sudo docker build -f ./dockerfile.builder -t ${DOCKER_REGISTRY}/builder .
	sudo docker push ${DOCKER_REGISTRY}/builder
	sudo docker rmi ${DOCKER_REGISTRY}/builder

.PHONY:build\:app
build\:app:
	sudo docker build -f ./dockerfile -t  ${DOCKER_REGISTRY}/app .
	sudo docker push ${DOCKER_REGISTRY}/app

.PHONY:build\:all
build\:all:
	build\:base
	build\:app

.PHONY:docker\:run
docker\:run:
	sudo docker run -itd --name fastapi_demo -p 8005:8080 --restart=always ${DOCKER_REGISTRY}/app

.PHONY:create\:sql
create\:sql:
	python db/create_new_migration.py

.PHONY:test
test:
	 export PYTHONPATH=$PYTHONPATH:`pwd` && python ./testcase/run_test.py

.PHONY:apply\:kind
apply\:kind:
	kubectl config use-context kind-kind
	kubectl apply -f ./deployments/test_deplyment.yaml

.PHONY:run\:celery
run\:celery:
	celery -A cmd_.celery.main worker --loglevel=info
	#celery beat -A cmd_.celery.main --loglevel=info