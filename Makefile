.PHONY: release

clean_fd:
	rm -rf release/floppydog.pyxapp
	rm -rf dist

clean_pf:
	rm -rf release/floppydog.pyxapp
	rm -rf dist

floppydog: clean_fd
	mkdir -p release
	mkdir -p dist/Assets
	cp flappydog.py dist/
	cp lib.py dist/
	cp Assets/flappydogs.pyxres dist/Assets/
	pyxel package ./dist dist/flappydog.py
	mv dist.pyxapp release/floppydog.pyxapp
	rm -rf dist

pathfinding: clean_pf
	mkdir -p release
	mkdir -p dist/Assets
	cp pathfinding.py dist/
	cp lib.py dist/
	cp Assets/pathfinding.pyxres dist/Assets/
	pyxel package ./dist dist/pathfinding.py
	mv dist.pyxapp release/pathfinding.pyxapp
	rm -rf dist
