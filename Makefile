#!make

include .env
export

SRC_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

deploy: rsync install_deps patch_db

install_deps:
	export $$(cat .env | grep -v '^#' | xargs) && \
	ssh $$RPI_HOST "cd $${RPI_TARGET_DIR} && pip install --user -qr requirements.txt"

patch_db:
	export $$(cat .env | grep -v '^#' | xargs) && \
		ssh $$RPI_HOST "cd $${RPI_TARGET_DIR} && ~/.local/bin/alembic upgrade head"

rsync:
	rsync -e ssh -avz --delete --exclude='.git' --exclude='*.pyc' --exclude='chilli.db' --exclude='tags' ${SRC_DIR} ${RPI_HOST}:${RPI_TARGET_DIR}/

