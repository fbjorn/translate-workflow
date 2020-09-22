WF_DIR = ${HOME}/Documents/Alfred/Alfred.alfredpreferences/workflows/translate-workflow
SRC = conf.py main.py info.plist lib icon.png

all: pip link

pip:
	python2 -m pip install --upgrade pip
	python2 -m pip install --target=./lib -r _requirements.txt

link:
	mkdir -p "${WF_DIR}"
	for f in ${SRC} ; do \
  		ln -sf "${PWD}/$$f" "${WF_DIR}/$$f"; \
  	done

clean:
	for f in ${SRC} ; do \
  		unlink "${WF_DIR}/$$f"; \
  	done
