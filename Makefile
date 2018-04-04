# author: Daichi Teruya

POSCLIB=./stitcher/clib/

MAKE=make

.PHONY: all
all: clib

.PHONY: clib
clib:
	$(MAKE) -C $(POSCLIB)

.PHONY: clean
clean:
	$(MAKE) -C $(POSCLIB) clean
	$(RM) ./*.png
