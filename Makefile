.PHONY: all generate model analyze test serve
all: generate model analyze test package
generate:
	python src/generate.py
model:
	dbt build --profiles-dir .
analyze:
	python src/analyze.py
test:
	python -m unittest discover -s tests -v
serve:
	python -m http.server 8000 --directory docs
package:
	python src/package.py

