prog ?= vadd
AVL?= 10
VLEN ?=32
COMP_OPTS = -static -mcmodel=medany -std=gnu99 -O2 -ffast-math -O2 -fno-common -Wall -march=rv32imacv
LINK_OPTS = -static -nostdlib -nostartfiles -lm -lgcc -T ${PROG_PATH}/link.ld
SCRIPTS_PATH=./py_scripts
PROG_PATH=./programs
BIN_PATH=./programs_bin
HAMMER_PATH?=/home/abal/hammer_vector

update_AVL:
	python3 ${SCRIPTS_PATH}/change_AVL.py ${PROG_PATH}/${prog}.c ${AVL}

compile_prog:
	riscv32-unknown-elf-gcc -o ${BIN_PATH}/${prog}.elf ${PROG_PATH}/${prog}.c ${PROG_PATH}/${prog}.S ${COMP_OPTS} ${LINK_OPTS}
	riscv32-unknown-elf-objdump -D ${BIN_PATH}/${prog}.elf > ${PROG_PATH}/${prog}.dasm

simulate_py:
	python3 ${SCRIPTS_PATH}/calc_speed_interactive.py ${HAMMER_PATH} ${PROG_PATH}/${prog}.dasm ${BIN_PATH}/${prog}.elf ${VLEN}

build_hammer:
	cd ${HAMMER_PATH} &&\
	meson setup builddir --native-file native-file.txt --buildtype release -Dspike_install_dir=${RISCV} &&\
	meson compile -C builddir

recompile_hammer:
	cd ${HAMMER_PATH} &&\
	meson compile -C builddir
