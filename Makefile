ANSERINI_CLASSPATH_PREFIX = anserini-ltr/target/anserini-ltr-1.0-SNAPSHOT.jar

install: install-anserini
	echo "install complete"

tests:
	nosetests

checkout-submodules:
	git submodule update --init --recursive

install-anserini: checkout-submodules
	cd third-party/anserini && mvn -Dmaven.javadoc.skip=true -Dgpg.skip clean package appassembler:assemble install 

python3-shell-with-correct-environment:
	python3 -i -c "import train;"
