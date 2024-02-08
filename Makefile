all:
	mkdir -p dist
	PYTHONIOENCODING=utf-8 python md2gv.py > dist/a.gv