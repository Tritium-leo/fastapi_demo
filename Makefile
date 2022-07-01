.PHONY:init
init:
	python -m pip install --upgrade pip
	pip install -r ./requirements.txt

.PHONY:run
run:
	gunicorn main:app -c config/config.py

.PHONY:build
build\:base:
	pip freeze> requirements.txt
	#sudo docker rmi testproject/builder
	sudo docker build -f ./dockerfile.builder -t testproject/builder .
	#sudo docker push testproject/builder

.PHONY:build\:app
build\:app:
	sudo docker build -f ./dockerfile -t  testproject/app .
	#sudo docker push testproject/app


.PHONY:build\:all
build\:all:
	build\:base
	build\:app

.PHONY:docker\:run
docker\:run:
	sudo docker run -d --name testproject_app -p 8080:8080 --restart=always testproject/app

.PHONY:create\:sql
create\:sql:
	python db/create_new_migration.py