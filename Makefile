ANSERINI_CLASSPATH_PREFIX = anserini-ltr/target/anserini-ltr-1.0-SNAPSHOT.jar

PYTHON3 = $(CURDIR)/$(VENV-DIR)/bin/python3
PIP3 = $(CURDIR)/$(VENV-DIR)/bin/pip3

VENV-DIR = .venv

install: install-anserini
	echo "install complete"

tests: install-nose
	$(VENV-DIR)/bin/nosetests

checkout-submodules:
	git submodule update --init --recursive

install-anserini: checkout-submodules
	cd third-party/anserini && mvn -Dmaven.javadoc.skip=true -Dgpg.skip clean package appassembler:assemble install 

python3-shell-with-correct-environment:
	"$(PYTHON3)" -i -c "import train;"

install-nose: $(VENV-DIR) checkout-submodules
	"$(PIP3)" install -r pip-testing-packages.txt

$(VENV-DIR):
	python3 -m venv .venv &&\
	"$(PIP3)" install --upgrade pip
