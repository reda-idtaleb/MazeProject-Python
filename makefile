.PHONY: dependency

%.x: install
	:

install:
	pip install rich pyfiglet

run: dependency.x 	
	python3 src/main.py 

