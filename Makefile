# Run tests
test:
	@pip install .[test]
	@PYTHONPATH=src/ pytest \
      --cov src/v2_samplesheet_maker \
      --capture=no | \
      tee coverage_report.txt

# Run build
build_package:
	@pip install .[build]
	@python3 -m build

# Install package
install:
	@pip install .

# Push to test pypi
push_test_pypi:
	@pip install .[deploy]
	@python3 -m twine upload --repository testpypi dist/* --verbose

# Install from test pypi
install_test_pypi:
	@pip install \
		--index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple/ \
		v2-samplesheet-maker==${V2_SAMPLESHEET_MAKER_VERSION}
	@v2-samplesheet-maker --help

# Install to pypi
push_pypi:
	@pip install .[deploy]
	@python3 -m twine upload --repository pypi dist/* --verbose

install_pypi:
	@pip install \
		--index-url https://pypi.org/simple/ \
		v2-samplesheet-maker==${V2_SAMPLESHEET_MAKER_VERSION}
	@v2-samplesheet-maker --help
