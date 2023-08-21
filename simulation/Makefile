.PHONY = all simulate
SHELL:=/bin/bash -O extglob
SIM_EXE:=sipo_piso.o
all: sim_iv

help:
	@echo -e "For Cleaning:"
	@echo -e "Delete Unnecessary Files:\tmake clean"
	@echo -e "For Simulation:"
	@echo -e "Cadence Incisive/Xcelium:\tmake sim_inc"
	@echo -e "Iverilog:\t\t\tmake sim_iv\n"
clean: 
	@echo -e "Cleaning Files..." 
	@rm -rvf !("Makefile"|*.f)
	@rm -rvf .simvision

sim_inc: clean
	@echo -e "Simulating Using Cadence Incisive/Xcelium..." 
	@irun -f files_rtl.f -access +rwc -incdir ../rtl -timescale 1ns/1ps -notimingcheck -overwrite

sim_iv: clean vvp_cmd
	gtkwave sipo_piso.vcd
vvp_cmd: iverilog_cmd
	vvp $(SIM_EXE)
iverilog_cmd:
	@echo "Simulating Using Iverilog..." 
	@rm -rvf !("Makefile"|*.f)
	@rm -rvf .simvision
	@iverilog -f files_rtl.f -o $(SIM_EXE) -I../rtl
