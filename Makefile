setup:
	# python2 -m virtualenv venv
	python3 -m venv venv; \
	./venv/bin/pip install --upgrade pip; \
	./venv/bin/pip install -r dev-requirements.txt

install:
	./venv/bin/pip install -e ./

uninstall:
	./venv/bin/pip uninstall logctl -y

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
	find . -name "venv" -print0 | xargs -0 rm -rf
	find . -name "__pycache__" -print0 | xargs -0 rm -rf
	find . -name "*.egg-info" -print0 | xargs -0 rm -rf
	find . -name "*.retry" -print0 | xargs -0 rm -rf
