# author: Daichi Teruya

TSTITCHER = PyStitcher.cpython-33m.so
STITCHERFILES = ./src/PyStitcher.cpp ./src/PyStitcher.hpp ./src/utility.hpp

GENFILES = $(TSTITCHER)

SETUPPY = setup.py
PYTHON = python3

.PHONY: all
all: $(GENFILES)

$(TSTITCHER): $(STITCHERFILES) $(SETUPPY)
	export PKG_CONFIG_PATH=/usr/lib/pkgconfig
	CC=g++ CXX=g++ $(PYTHON) setup.py build_ext -i

.PHONY: clean
clean:
	$(RM) -rf build/
	$(RM) $(GENFILES)
