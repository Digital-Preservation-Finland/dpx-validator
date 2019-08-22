test:
	python -m pytest -sv --maxfail=9999 --junitprefix=dpx-validator --junitxml=junit.xml tests

clean:
	git clean -Xf
