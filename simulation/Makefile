.PHONY = all simulate
SHELL:=/bin/bash -O extglob
all: sim

clean: 
	@echo "Deleting Files..." 
	@rm -rvf !("Makefile"|*.history|*.f|*.rcf|*.hex)
	@rm -rvf .simvision

sim: 
	@echo "Simulating Synthesis Netlist..." 
	@rm -rvf !("Makefile"|*.history|*.f|*.rcf|*.hex)
	@rm -rvf .simvision
	@xrun -f files_rtl.f -access +rwc -incdir ../rtl -timescale 1ns/1ps -notimingcheck -overwrite -gui
