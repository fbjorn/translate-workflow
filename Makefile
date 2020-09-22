WF_DIR = ${HOME}/Documents/Alfred/Alfred.alfredpreferences/workflows/translate-workflow
SRC = conf.py main.py info.plist lib icon.png

all: pip link

pip:
	python2 -m pip install wheel
	python2 -m pip install --upgrade pip
	python2 -m pip --version
	python2 -m pip install --target=./lib Alfred-Workflow==1.40.0

link:
	mkdir -p "${WF_DIR}"
	for f in ${SRC} ; do \
  		ln -sf "${PWD}/$$f" "${WF_DIR}/$$f"; \
  	done

clean:
	for f in ${SRC} ; do \
  		unlink "${WF_DIR}/$$f"; \
  	done
