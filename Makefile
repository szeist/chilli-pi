#!make

include .env
export

SRC_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

run: rsync remote_execute

deploy: rsync install_deps

remote_execute:
	export $$(cat .env | grep -v '^#' | xargs) && \
	ssh $$RPI_HOST "cd $${RPI_TARGET_DIR} && python chilli_pi.py"

install_deps:
	export $$(cat .env | grep -v '^#' | xargs) && \
	ssh $$RPI_HOST "cd $${RPI_TARGET_DIR} && pip install --user -qr requirements.txt"

rsync:
	rsync -e ssh -avz --delete --exclude='*.pyc' ${SRC_DIR} ${RPI_HOST}:${RPI_TARGET_DIR}/

