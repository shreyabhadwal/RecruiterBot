install:
	#install command
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	#format code command
	#black or yapf
	@echo "formatting code"
lint:
	#flake8 or pylint
test:
	#pytest
deploy:
	#deploy command
all: install lint test deploy