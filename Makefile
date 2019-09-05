test:
	python -m pytest -sv --maxfail=9999 --junitprefix=dpx-validator --junitxml=junit.xml tests

clean:
	git clean -Xf

coverage:
	python -m pytest -svvv --cov=dpx_validator --cov-fail-under=80 --cov-report=term-missing tests
