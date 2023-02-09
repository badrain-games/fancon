.PHONY: dist

clean:
	rm -rf release/floppydog.pyxapp
	rm -rf dist

dist: clean
	mkdir -p release
	mkdir -p dist/Assets
	cp flappydog.py dist/
	cp lib.py dist/
	cp Assets/flappydogs.pyxres dist/Assets/
	pyxel package ./dist dist/flappydog.py
	mv dist.pyxapp release/floppydog.pyxapp

